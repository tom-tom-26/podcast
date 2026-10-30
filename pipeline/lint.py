"""Check a Bundle before it is merged, rendered or published."""

import argparse
import sys
import time
from pathlib import Path

from pipeline._lib.bundle import bundle_problems


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")


def main(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    problems = bundle_problems(args.bundle)
    for problem in problems:
        print(f"{args.bundle.name}: {problem}")
    elapsed = time.perf_counter() - started
    print(
        f"lint {args.bundle.name}: {len(problems)} blocking, 0 warnings in {elapsed:.2f} s",
        file=sys.stderr,
    )
    return 1 if problems else 0
