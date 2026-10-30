"""Build the Pages site: the Feed, the Archive page, robots.txt, the Cover and the audio."""

import argparse
import re
import shutil
import struct
import sys
import time
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

import yaml

from pipeline._lib.archive import archive_html
from pipeline._lib.bundle import load_meta
from pipeline._lib.feed import build_feed, feed_problems
from pipeline._lib.github import GitHub
from pipeline._lib.live import live_problems
from pipeline._lib.registry import REGISTRY, load_registry

COVER_SIZE = 3000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_RGB = 2
ROBOTS = "User-agent: *\nDisallow: /\n"


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", required=True, help="the site's public URL")
    parser.add_argument("--repo", type=Path, default=Path("."), help="the repo checkout")
    parser.add_argument("--out", type=Path, default=Path("_site"), help="the folder to build in")
    parser.add_argument(
        "--check",
        action="store_true",
        help="build nothing; check the live site's HEAD and range answers and the Feed's guids",
    )


def main(args: argparse.Namespace, github=None) -> int:
    started = time.perf_counter()
    base = args.base_url.rstrip("/")
    episodes = load_registry((args.repo / REGISTRY).read_text(encoding="utf-8"))
    if args.check:
        problems = live_problems(base, episodes)
        for problem in problems:
            print(f"site check: {problem}", file=sys.stderr)
        print(
            f"site check {base}: {len(episodes)} Episodes, {len(problems)} problems "
            f"in {time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 1 if problems else 0

    github = github or GitHub.from_env()
    show = yaml.safe_load((args.repo / "config" / "show.yaml").read_text(encoding="utf-8"))
    roster = yaml.safe_load((args.repo / "config" / "voices.yaml").read_text(encoding="utf-8"))
    if args.out.exists() and any(args.out.iterdir()):
        print(f"site: {args.out} is not empty; build into a fresh folder", file=sys.stderr)
        return 1
    audio = args.out / "audio"
    audio.mkdir(parents=True, exist_ok=True)

    items = []
    for episode in reversed(episodes):
        bundle = args.repo / "bundles" / episode["bundle_id"]
        meta = load_meta(bundle)
        notes = (bundle / "show_notes.md").read_text(encoding="utf-8").rstrip()
        credit = roster["voices"].get(episode["voice"], {}).get("credit")
        if credit:
            notes += f"\n\n{credit}"
        published = datetime.fromisoformat(github.published_at(episode["episode_id"]))
        items.append(
            {
                "title": f"Episode {episode['number']}: {meta['title']}",
                "summary": meta["summary"],
                "notes": notes,
                "guid": episode["guid"],
                "url": f"{base}/audio/{episode['file']}",
                "bytes": episode["bytes"],
                "duration": episode["duration"],
                "published": published,
                # Q&As number as 7q to 7z, then 7z2, and are bonus items; Parts use a-c.
                "bonus": re.search("[q-z]", episode["number"]) is not None,
                "release_url": github.download_url(episode["episode_id"], episode["file"]),
            }
        )

    # Every Episode is in the Window until the Window ticket adds the size budget.
    for episode in episodes:
        try:
            github.download_asset(episode["episode_id"], episode["file"], audio / episode["file"])
        except RuntimeError as error:
            print(
                f"site: could not fetch {episode['file']} for {episode['episode_id']}: {error}; "
                "nothing deployed, Pages keeps the last good site",
                file=sys.stderr,
            )
            return 1
    fetched = sum(f.stat().st_size for f in audio.iterdir())
    print(
        f"site: fetched {len(episodes)} audio files, {fetched / 1e6:.1f} MB, "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )

    feed = build_feed(show, base, items)
    (args.out / "feed.xml").write_text(feed, encoding="utf-8")
    (args.out / "archive.html").write_text(archive_html(show, items), encoding="utf-8")
    (args.out / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    shutil.copy(args.repo / show["artwork"], args.out / "cover.png")

    problems = cover_problems(args.out / "cover.png") + feed_problems(feed, base, args.out)
    for problem in problems:
        print(f"site: {problem}", file=sys.stderr)
    print(
        f"site: Feed with {len(items)} Episodes, {len(problems)} blocking problems, "
        f"{time.perf_counter() - started:.1f} s in all",
        file=sys.stderr,
    )
    return 1 if problems else 0


def cover_problems(png: Path) -> list[str]:
    """Apple's rules for the Cover (research/04 section 4) that it breaks, one message each."""
    data = png.read_bytes()
    if not data.startswith(PNG_SIGNATURE) or data[12:16] != b"IHDR":
        return [f"{png.name}: not a PNG"]
    width, height, _, colour_type = struct.unpack(">IIBB", data[16:26])
    problems = []
    if width != height:
        problems.append(f"{png.name}: {width}x{height} is not square")
    elif width != COVER_SIZE:
        problems.append(f"{png.name}: {width}x{height}, expected {COVER_SIZE}x{COVER_SIZE}")
    if colour_type != PNG_RGB:
        problems.append(f"{png.name}: PNG colour type {colour_type}, expected RGB with no alpha")
    # An RGB PNG can still mark one colour transparent with a tRNS chunk.
    elif b"tRNS" in _chunk_types(data):
        problems.append(f"{png.name}: has a transparent colour (tRNS chunk)")
    return problems


def _chunk_types(data: bytes) -> Iterator[bytes]:
    at = len(PNG_SIGNATURE)
    while at + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[at : at + 8])
        yield kind
        at += length + 12  # length, type and CRC around the chunk data
