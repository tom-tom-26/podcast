"""Make an Episode from a Bundle and add it to the Episode registry."""

import argparse
import sys
import time
from pathlib import Path

from pipeline._lib.encode import encode_episode


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument("--wav", type=Path, required=True, help="the rendered WAV")
    parser.add_argument("--out-dir", type=Path, required=True, help="where the .m4a goes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only encode the .m4a: no Release, registry change or deploy",
    )


def main(args: argparse.Namespace) -> int:
    if not args.dry_run:
        print("pipeline publish: publishing without --dry-run is not built yet", file=sys.stderr)
        return 1
    started = time.perf_counter()
    m4a = args.out_dir / f"{args.bundle.name}.m4a"
    encode_episode(args.wav, m4a)
    print(
        f"publish {args.bundle.name}: dry run, encoded {m4a.stat().st_size} bytes "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )
    return 0
