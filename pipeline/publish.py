"""Make an Episode from a Bundle and add it to the Episode registry."""

import argparse
import functools
import re
import sys
import time
import uuid
from pathlib import Path

import yaml

from pipeline import render
from pipeline._lib.bundle import BUNDLE_ID, load_meta
from pipeline._lib.encode import duration_seconds, encode_episode
from pipeline._lib.gates import PACE_WPM, check_episode, transcribe
from pipeline._lib.github import GitHub
from pipeline._lib.lexicon import load_lexicon
from pipeline._lib.registry import (
    REGISTRY,
    NumberingError,
    dump_registry,
    episode_id,
    load_registry,
    number_episodes,
)
from pipeline._lib.roster import load_roster, with_credit
from pipeline._lib.synthesise import synthesise

ASR_REPORT = "asr_report.yaml"


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "bundle", type=Path, nargs="+", help="the Bundle folder, or every Part of one topic"
    )
    parser.add_argument(
        "--wav", type=Path, nargs="+", required=True, help="the rendered WAV of each Bundle"
    )
    parser.add_argument("--out-dir", type=Path, required=True, help="where the .m4a goes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only encode and gate the .m4a: no Release, registry change or deploy",
    )
    parser.add_argument(
        "--rerender",
        action="store_true",
        help="re-render published Episodes as -v2 (then -v3) in their own Releases, same guid",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="the repo checkout, for the voice roster, pacing config and Lexicon",
    )


def main(
    args: argparse.Namespace,
    github=None,
    transcribe=transcribe,
    encode=encode_episode,
    synthesise=synthesise,
) -> int:
    started = time.perf_counter()
    bundle_ids = [bundle.name for bundle in args.bundle]
    name = " ".join(bundle_ids)
    if len(args.wav) != len(args.bundle):
        print(
            f"publish {name}: {len(args.bundle)} Bundles but {len(args.wav)} WAVs",
            file=sys.stderr,
        )
        return 1
    # Every Release's report has the same name, so each Part gets a folder of its own.
    out_dirs = [
        args.out_dir if len(args.bundle) == 1 else args.out_dir / bundle_id
        for bundle_id in bundle_ids
    ]
    gate = functools.partial(
        _encode_and_gate,
        repo=args.repo,
        transcribe=transcribe,
        encode=encode,
        synthesise=synthesise,
    )
    if args.dry_run:
        passed = [
            gate(bundle, wav, out / f"{bundle.name}.m4a", bundle.name)
            for bundle, wav, out in zip(args.bundle, args.wav, out_dirs, strict=True)
        ]
        if not all(passed):
            return 1
        print(
            f"publish {name}: dry run, encoded and gated {len(passed)} Bundles in "
            f"{time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 0

    for bundle_id in bundle_ids:
        if not BUNDLE_ID.fullmatch(bundle_id):
            print(f"publish {bundle_id}: folder name is not a Bundle id", file=sys.stderr)
            return 1
    github = github or GitHub.from_env()
    text, sha = github.read_file(REGISTRY)
    episodes = load_registry(text)
    if args.rerender:
        return _rerender(args, github, gate, episodes, sha, out_dirs, started)
    for episode in episodes:
        if episode["bundle_id"] in bundle_ids:
            print(
                f"publish {episode['bundle_id']}: already published as {episode['episode_id']}",
                file=sys.stderr,
            )
            return 1
    metas = [load_meta(bundle) for bundle in args.bundle]
    try:
        numbers = number_episodes(metas, episodes)
    except NumberingError as error:
        print(f"publish {name}: {error}; nothing published", file=sys.stderr)
        return 1
    ids = [episode_id(n, b) for n, b in zip(numbers, bundle_ids, strict=True)]
    m4as = [out / f"{episode}.m4a" for out, episode in zip(out_dirs, ids, strict=True)]

    # Every Part is gated before any Release exists, so one failing Part publishes none.
    reports = [
        gate(bundle, wav, m4a, episode)
        for bundle, wav, m4a, episode in zip(args.bundle, args.wav, m4as, ids, strict=True)
    ]
    if not all(reports):
        if len(ids) > 1:
            print(f"publish {name}: a Part failed, so no Part is published", file=sys.stderr)
        return 1

    roster = load_roster(args.repo)
    releases = []
    for bundle, meta, number, episode, m4a, report in zip(
        args.bundle, metas, numbers, ids, m4as, reports, strict=True
    ):
        notes = with_credit(
            (bundle / "show_notes.md").read_text(encoding="utf-8"), roster, meta["voice"]
        )
        release = github.create_release(episode, f"Episode {number}: {meta['title']}", notes)
        github.upload_asset(release, m4a)
        github.upload_asset(release, report)
        releases.append(release)
    if not _uploads_match(github, releases, ids, m4as, reports):
        return 1
    for release in releases:
        github.publish_release(release)
    print(f"publish {' '.join(ids)}: Releases published, upload sizes checked", file=sys.stderr)

    for bundle_id, meta, number, episode, m4a in zip(
        bundle_ids, metas, numbers, ids, m4as, strict=True
    ):
        episodes.append(
            {
                "number": number,
                "episode_id": episode,
                "bundle_id": bundle_id,
                "guid": str(uuid.uuid4()),
                "voice": meta["voice"],
                "file": m4a.name,
                "bytes": m4a.stat().st_size,
                "duration": duration_seconds(m4a),
            }
        )
    github.commit_file(REGISTRY, dump_registry(episodes), sha, f"Publish {', '.join(ids)}")
    print(
        f"publish {' '.join(ids)}: registry entries {', '.join(numbers)} committed in one "
        f"commit, {time.perf_counter() - started:.1f} s in all",
        file=sys.stderr,
    )
    return 0


def _rerender(args, github, gate, episodes, sha, out_dirs, started) -> int:
    """Re-render published Episodes into their own Releases as the next free -vN file, keeping
    every earlier file and the guid, then move each registry entry to the new file in one
    commit. Every Episode is gated and its upload checked before the registry changes."""
    entries = {episode["bundle_id"]: episode for episode in episodes}
    for bundle in args.bundle:
        if bundle.name not in entries:
            print(
                f"publish {bundle.name}: {bundle.name} is not published, so there is nothing to "
                "re-render",
                file=sys.stderr,
            )
            return 1
    found = [entries[bundle.name] for bundle in args.bundle]
    ids = [entry["episode_id"] for entry in found]
    releases = [github.release_id(episode) for episode in ids]
    # The next number free in the Release, not the registry's, since a re-render that failed
    # its upload check leaves its file behind and GitHub refuses a second asset of that name.
    versions = [
        _next_version(episode, github.asset_sizes(release))
        for episode, release in zip(ids, releases, strict=True)
    ]
    m4as = [
        out / f"{episode}-v{version}.m4a"
        for out, episode, version in zip(out_dirs, ids, versions, strict=True)
    ]
    reports = [
        gate(bundle, wav, m4a, episode)
        for bundle, wav, m4a, episode in zip(args.bundle, args.wav, m4as, ids, strict=True)
    ]
    if not all(reports):
        if len(ids) > 1:
            print(f"publish {' '.join(ids)}: one failed, so none is re-rendered", file=sys.stderr)
        return 1
    reports = [
        report.replace(report.with_name(f"{report.stem}-v{version}{report.suffix}"))
        for report, version in zip(reports, versions, strict=True)
    ]
    for release, m4a, report in zip(releases, m4as, reports, strict=True):
        github.upload_asset(release, m4a)
        github.upload_asset(release, report)
    if not _uploads_match(github, releases, ids, m4as, reports):
        return 1

    roster = load_roster(args.repo)
    for bundle, entry, release, m4a in zip(args.bundle, found, releases, m4as, strict=True):
        meta = load_meta(bundle)
        notes = with_credit(
            (bundle / "show_notes.md").read_text(encoding="utf-8"), roster, meta["voice"]
        )
        github.update_release(release, f"Episode {entry['number']}: {meta['title']}", notes)
        entry.update(
            voice=meta["voice"],
            file=m4a.name,
            bytes=m4a.stat().st_size,
            duration=duration_seconds(m4a),
        )
    done = ", ".join(f"{e} as v{v}" for e, v in zip(ids, versions, strict=True))
    github.commit_file(REGISTRY, dump_registry(episodes), sha, f"Re-render {done}")
    print(
        f"publish: re-rendered {done}, guids kept, registry committed, "
        f"{time.perf_counter() - started:.1f} s in all",
        file=sys.stderr,
    )
    return 0


def _next_version(episode: str, assets: dict[str, int]) -> int:
    # The first render is v1 with no suffix.
    taken = [
        int(found[1] or 1)
        for name in assets
        if (found := re.fullmatch(rf"{re.escape(episode)}(?:-v(\d+))?\.m4a", name))
    ]
    return max(taken, default=1) + 1


def _uploads_match(github, releases, ids, m4as, reports) -> bool:
    """Whether every uploaded file has the local file's byte size, said per file if not."""
    for release, episode, m4a, report in zip(releases, ids, m4as, reports, strict=True):
        uploaded = github.asset_sizes(release)
        for asset in (m4a, report):
            if uploaded.get(asset.name) != asset.stat().st_size:
                print(
                    f"publish {episode}: Release has {asset.name} at "
                    f"{uploaded.get(asset.name)} bytes but the local file is "
                    f"{asset.stat().st_size}; the registry is unchanged",
                    file=sys.stderr,
                )
                return False
    return True


def _encode_and_gate(
    bundle: Path, wav: Path, m4a: Path, name: str, repo: Path, transcribe, encode, synthesise
) -> Path | None:
    """Encode the WAV and gate the .m4a. An ASR fail re-renders the chunk it names once and
    gates again; any other fail, or a second one, stops the run. Gives the ASR report."""
    meta = load_meta(bundle)
    lexicon = load_lexicon(repo, meta)
    for attempt in range(2):
        started = time.perf_counter()
        encode(wav, m4a)
        chunk_map = yaml.safe_load(render.chunk_map_path(wav).read_text(encoding="utf-8"))
        verdict = check_episode(
            m4a, chunk_map, transcribe(m4a), lexicon, meta.get("wpm_budget") or PACE_WPM
        )
        for warning in verdict.warnings:
            print(f"publish {name}: {warning}; a warning only", file=sys.stderr)
        for failure in verdict.failures:
            where = ""
            if failure.chunk is not None:
                chunk = chunk_map["chunks"][failure.chunk]
                where = f" at chunk {failure.chunk} ({chunk['segment']}: {chunk['text'][:60]!r})"
            print(
                f"publish {name}: {failure.gate} gate failed{where}: {failure.detail}",
                file=sys.stderr,
            )
        if not verdict.failures:
            measures = verdict.measures
            print(
                f"publish {name}: gates passed in {time.perf_counter() - started:.1f} s "
                f"(missing run {measures['missing_run']}, silence "
                f"{measures['longest_silence']:.1f} s, {measures['loudness']:.1f} LUFS, "
                f"{measures['true_peak']:.1f} dBTP)",
                file=sys.stderr,
            )
            report = m4a.parent / ASR_REPORT
            report.write_text(
                yaml.safe_dump(
                    {"episode": name, **verdict.asr_report}, sort_keys=False, allow_unicode=True
                ),
                encoding="utf-8",
            )
            return report
        failure = verdict.asr_failure()
        # A re-render can't fix a whole-file fail, so only a lone ASR fail is worth one.
        if attempt or failure is None or len(verdict.failures) > 1:
            break
        print(f"publish {name}: re-rendering chunk {failure.chunk} once", file=sys.stderr)
        render.rerender_chunk(bundle, wav, failure.chunk, repo, synthesise)
    print(f"publish {name}: gates failed; nothing published", file=sys.stderr)
    return None
