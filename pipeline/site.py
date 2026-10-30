"""Build the Feed for GitHub Pages."""

import argparse
import struct
import sys
from collections.abc import Iterator
from pathlib import Path

COVER_SIZE = 3000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_RGB = 2


def add_arguments(parser: argparse.ArgumentParser) -> None:
    pass


def main(args: argparse.Namespace) -> int:
    print("pipeline site: not built yet", file=sys.stderr)
    return 1


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
