"""Check a Bundle before it is merged, rendered or published."""

import sys


def main() -> int:
    print("pipeline lint: not built yet", file=sys.stderr)
    return 1
