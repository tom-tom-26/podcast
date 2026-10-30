"""Make an Episode from a Bundle and add it to the Episode registry."""

import argparse
import sys
import time
import uuid
from pathlib import Path

from pipeline._lib.bundle import BUNDLE_ID, load_meta
from pipeline._lib.encode import duration_seconds, encode_episode
from pipeline._lib.github import GitHub
from pipeline._lib.registry import REGISTRY, dump_registry, load_registry, next_number


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument("--wav", type=Path, required=True, help="the rendered WAV")
    parser.add_argument("--out-dir", type=Path, required=True, help="where the .m4a goes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only encode the .m4a: no Release, registry change or deploy",
    )


def main(args: argparse.Namespace, github=None) -> int:
    started = time.perf_counter()
    bundle_id = args.bundle.name
    if args.dry_run:
        m4a = args.out_dir / f"{bundle_id}.m4a"
        encode_episode(args.wav, m4a)
        print(
            f"publish {bundle_id}: dry run, encoded {m4a.stat().st_size} bytes "
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
    encode_episode(args.wav, m4a)
    size = m4a.stat().st_size
    print(f"publish {episode_id}: encoded {size} bytes", file=sys.stderr)

    meta = load_meta(args.bundle)
    notes = (args.bundle / "show_notes.md").read_text(encoding="utf-8")
    release = github.create_release(episode_id, f"Episode {number}: {meta['title']}", notes)
    github.upload_asset(release, m4a)
    uploaded = github.asset_sizes(release).get(m4a.name)
    if uploaded != size:
        print(
            f"publish {episode_id}: draft Release has {m4a.name} at {uploaded} bytes but the "
            f"local file is {size}; nothing published and the registry is unchanged",
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
