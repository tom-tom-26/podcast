"""Make an Episode from a Bundle and add it to the Episode registry."""

import argparse
import sys
import time
import uuid
from pathlib import Path

import yaml

from pipeline import render
from pipeline._lib.bundle import BUNDLE_ID, load_meta
from pipeline._lib.encode import duration_seconds, encode_episode
from pipeline._lib.gates import check_episode, transcribe
from pipeline._lib.github import GitHub
from pipeline._lib.lexicon import load_lexicon
from pipeline._lib.registry import REGISTRY, dump_registry, load_registry, next_number
from pipeline._lib.roster import load_roster, with_credit
from pipeline._lib.synthesise import synthesise

ASR_REPORT = "asr_report.yaml"


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument("--wav", type=Path, required=True, help="the rendered WAV")
    parser.add_argument("--out-dir", type=Path, required=True, help="where the .m4a goes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only encode and gate the .m4a: no Release, registry change or deploy",
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
    bundle_id = args.bundle.name
    if args.dry_run:
        m4a = args.out_dir / f"{bundle_id}.m4a"
        if not _encode_and_gate(args, m4a, bundle_id, transcribe, encode, synthesise):
            return 1
        print(
            f"publish {bundle_id}: dry run, encoded {m4a.stat().st_size} bytes and gated "
            f"in {time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 0

    if not BUNDLE_ID.fullmatch(bundle_id):
        print(f"publish {bundle_id}: folder name is not a Bundle id", file=sys.stderr)
        return 1
    github = github or GitHub.from_env()
    text, sha = github.read_file(REGISTRY)
    episodes = load_registry(text)
    for episode in episodes:
        if episode["bundle_id"] == bundle_id:
            print(
                f"publish {bundle_id}: already published as {episode['episode_id']}",
                file=sys.stderr,
            )
            return 1

    number = next_number(episodes)
    slug = bundle_id.split("-", 3)[3]
    episode_id = f"ep-{number:03d}-{slug}"
    m4a = args.out_dir / f"{episode_id}.m4a"
    report = _encode_and_gate(args, m4a, episode_id, transcribe, encode, synthesise)
    if not report:
        return 1
    size = m4a.stat().st_size

    meta = load_meta(args.bundle)
    notes = with_credit(
        (args.bundle / "show_notes.md").read_text(encoding="utf-8"),
        load_roster(args.repo),
        meta["voice"],
    )
    release = github.create_release(episode_id, f"Episode {number}: {meta['title']}", notes)
    github.upload_asset(release, m4a)
    github.upload_asset(release, report)
    uploaded = github.asset_sizes(release)
    for asset in (m4a, report):
        if uploaded.get(asset.name) != asset.stat().st_size:
            print(
                f"publish {episode_id}: draft Release has {asset.name} at "
                f"{uploaded.get(asset.name)} bytes but the local file is {asset.stat().st_size}; "
                "nothing published and the registry is unchanged",
                file=sys.stderr,
            )
            return 1
    github.publish_release(release)
    print(f"publish {episode_id}: Release published, upload size checked", file=sys.stderr)

    episodes.append(
        {
            "number": str(number),
            "episode_id": episode_id,
            "bundle_id": bundle_id,
            "guid": str(uuid.uuid4()),
            "voice": meta["voice"],
            "file": m4a.name,
            "bytes": size,
            "duration": duration_seconds(m4a),
        }
    )
    github.commit_file(REGISTRY, dump_registry(episodes), sha, f"Publish {episode_id}")
    print(
        f"publish {episode_id}: registry entry {number} committed, "
        f"{time.perf_counter() - started:.1f} s in all",
        file=sys.stderr,
    )
    return 0


def _encode_and_gate(args, m4a: Path, name: str, transcribe, encode, synthesise) -> Path | None:
    """Encode the WAV and gate the .m4a. An ASR fail re-renders the chunk it names once and
    gates again; any other fail, or a second one, stops the run. Gives the ASR report."""
    meta = load_meta(args.bundle)
    lexicon = load_lexicon(args.repo, meta)
    for attempt in range(2):
        started = time.perf_counter()
        encode(args.wav, m4a)
        chunk_map = yaml.safe_load(render.chunk_map_path(args.wav).read_text(encoding="utf-8"))
        verdict = check_episode(
            m4a, chunk_map, transcribe(m4a), lexicon, meta.get("wpm_budget") or 165
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
        if attempt or failure is None:
            break
        print(f"publish {name}: re-rendering chunk {failure.chunk} once", file=sys.stderr)
        render.rerender_chunk(args.bundle, args.wav, failure.chunk, args.repo, synthesise)
    print(f"publish {name}: gates failed; nothing published", file=sys.stderr)
    return None
