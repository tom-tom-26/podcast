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
from pipeline._lib.roster import load_roster, with_credit
from pipeline._lib.rules import CORRECTION_NOTE
from pipeline._lib.window import MB, PIN_LIST, choose_window, load_pins

COVER_SIZE = 3000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_RGB = 2
ROBOTS = "User-agent: *\nDisallow: /\n"
TEST_REGISTRY = "config/test_episodes.yaml"
TEST_FEED = "test/feed.xml"


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
    tests = load_registry((args.repo / TEST_REGISTRY).read_text(encoding="utf-8"))
    rules = yaml.safe_load((args.repo / "config" / "site.yaml").read_text(encoding="utf-8"))
    pins = load_pins(args.repo / PIN_LIST)
    budget = rules["budget_mb"] * MB
    window = choose_window(episodes, pins, budget)
    in_feed = episodes if rules["repoint"] else window
    if args.check:
        feeds = {"feed.xml": in_feed} | ({TEST_FEED: tests} if tests else {})
        problems = live_problems(base, feeds)
        for problem in problems:
            print(f"site check: {problem}", file=sys.stderr)
        print(
            f"site check {base}: {len(in_feed)} Episodes, {len(tests)} test Episodes, "
            f"{len(problems)} problems in {time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 1 if problems else 0

    github = github or GitHub.from_env()
    show = yaml.safe_load((args.repo / "config" / "show.yaml").read_text(encoding="utf-8"))
    roster = load_roster(args.repo)
    if args.out.exists() and any(args.out.iterdir()):
        print(f"site: {args.out} is not empty; build into a fresh folder", file=sys.stderr)
        return 1

    known = {episode["episode_id"] for episode in episodes}
    for pin in pins:
        if pin not in known:
            print(f"site: pinned {pin} is not in the registry; ignored", file=sys.stderr)
    window_bytes = sum(episode["bytes"] for episode in window)
    dropped = [episode["episode_id"] for episode in episodes if episode not in window]
    if dropped or window_bytes > budget:
        print(
            f"site: warning: the Window is {window_bytes / MB:.1f} MB against a "
            f"{rules['budget_mb']} MB budget; dropped {', '.join(dropped) or 'nothing'}"
            + (", which stay in the Feed on their Release URL" if rules["repoint"] else ""),
            file=sys.stderr,
        )

    # A Feed item's audio is a copy on the site, or else the Release download URL, which is
    # stable; it redirects to a signed URL that expires, which must never go in a Feed.
    fetch = [(episode, f"audio/{episode['file']}") for episode in window]
    fetch += [(e, f"test/audio/{e['file']}") for e in tests if not _on_release(e)]
    for episode, path in fetch:
        (args.out / path).parent.mkdir(parents=True, exist_ok=True)
        try:
            github.download_asset(episode["episode_id"], episode["file"], args.out / path)
        except RuntimeError as error:
            print(
                f"site: could not fetch {episode['file']} for {episode['episode_id']}: {error}; "
                "nothing deployed, Pages keeps the last good site",
                file=sys.stderr,
            )
            return 1
    fetched_bytes = sum(episode["bytes"] for episode, _ in fetch)
    print(
        f"site: fetched {len(fetch)} audio files, {fetched_bytes / MB:.1f} MB, "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )

    def item(episode, url, title_prefix=""):
        bundle = args.repo / "bundles" / episode["bundle_id"]
        meta = load_meta(bundle)
        written = (bundle / "show_notes.md").read_text(encoding="utf-8")
        notes = with_credit(written, roster, episode["voice"])
        return {
            "title": f"{title_prefix}Episode {episode['number']}: {meta['title']}",
            "summary": meta["summary"],
            "notes": notes,
            # Outside the Window the Archive page is the only place a correction shows.
            "corrections": CORRECTION_NOTE.findall(written),
            "guid": episode["guid"],
            "url": url,
            "bytes": episode["bytes"],
            "duration": episode["duration"],
            "published": datetime.fromisoformat(github.published_at(episode["episode_id"])),
            # Q&As number as 7q to 7z, then 7z2, and are bonus items; Parts use a-c.
            "bonus": re.search("[q-z]", episode["number"]) is not None,
            "download_url": release_url(episode),
        }

    def release_url(episode):
        return github.download_url(episode["episode_id"], episode["file"])

    items, in_feed_items = [], []
    for episode in reversed(episodes):
        on_site = episode in window
        items.append(
            item(episode, f"{base}/audio/{episode['file']}" if on_site else release_url(episode))
        )
        if episode in in_feed:
            in_feed_items.append(items[-1])
    feed = build_feed(show, base, in_feed_items)
    (args.out / "feed.xml").write_text(feed, encoding="utf-8")
    (args.out / "archive.html").write_text(archive_html(show, items), encoding="utf-8")
    (args.out / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    shutil.copy(args.repo / show["artwork"], args.out / "cover.png")
    repointed_urls = {release_url(e) for e in in_feed if e not in window}
    problems = cover_problems(args.out / "cover.png") + feed_problems(
        feed, base, args.out, repointed_urls
    )

    if tests:
        test_items = [
            item(
                episode,
                release_url(episode)
                if _on_release(episode)
                else f"{base}/test/audio/{episode['file']}",
                title_prefix="TEST ",
            )
            for episode in reversed(tests)
        ]
        test_feed = build_feed({**show, "title": f"TEST {show['title']}"}, base, test_items)
        (args.out / TEST_FEED).parent.mkdir(exist_ok=True)
        (args.out / TEST_FEED).write_text(test_feed, encoding="utf-8")
        test_release_urls = {release_url(e) for e in tests if _on_release(e)}
        problems += [
            f"{TEST_FEED}: {problem}"
            for problem in feed_problems(test_feed, base, args.out, test_release_urls)
        ]
        # A test item under a real guid would stand in for that Episode in a listener's app.
        real = {episode["guid"] for episode in episodes}
        problems += [
            f"{TEST_FEED}: {e['episode_id']} reuses the guid {e['guid']} of a real Episode"
            for e in tests
            if e["guid"] in real
        ]

    site_bytes = sum(f.stat().st_size for f in args.out.rglob("*") if f.is_file())
    if site_bytes > rules["ceiling_mb"] * MB:
        problems.append(
            f"the site is {site_bytes / MB:.1f} MB, over the {rules['ceiling_mb']} MB ceiling; "
            "pin fewer Episodes"
        )
    for problem in problems:
        print(f"site: {problem}", file=sys.stderr)
    print(
        f"site: Feed with {len(in_feed_items)} Episodes, {len(window)} in the Window, "
        f"{len(tests)} test Episodes, site {site_bytes / MB:.1f} MB, "
        f"{len(problems)} blocking problems, {time.perf_counter() - started:.1f} s in all",
        file=sys.stderr,
    )
    return 1 if problems else 0


def _on_release(test_episode: dict) -> bool:
    # For the Apple test: the item points at its Release, not a copy on the site.
    return test_episode.get("enclosure") == "release"


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
