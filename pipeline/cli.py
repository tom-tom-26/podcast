import argparse

from pipeline import lint, publish, render, site

ENTRY_POINTS = {"lint": lint, "render": render, "publish": publish, "site": site}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pipeline")
    commands = parser.add_subparsers(dest="entry_point", required=True)
    for name, module in ENTRY_POINTS.items():
        commands.add_parser(name, help=module.__doc__, description=module.__doc__)
    args = parser.parse_args(argv)
    return ENTRY_POINTS[args.entry_point].main()
