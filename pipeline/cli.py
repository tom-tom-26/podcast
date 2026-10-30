import argparse

from pipeline import lint, merge, publish, render, report, site

ENTRY_POINTS = {
    "lint": lint,
    "render": render,
    "publish": publish,
    "site": site,
    "report": report,
    "merge": merge,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pipeline")
    commands = parser.add_subparsers(dest="entry_point", required=True)
    for name, module in ENTRY_POINTS.items():
        command = commands.add_parser(name, help=module.__doc__, description=module.__doc__)
        module.add_arguments(command)
    args = parser.parse_args(argv)
    return ENTRY_POINTS[args.entry_point].main(args)
