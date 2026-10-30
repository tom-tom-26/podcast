"""Check a Bundle before it is merged, rendered or published."""

import argparse
import os
import sys
import time
from pathlib import Path

import yaml

from pipeline._lib.bundle import bundle_problems, load_meta
from pipeline._lib.lexicon import load_lexicon, phonemize
from pipeline._lib.rules import (
    claim_problems,
    ledger_ids,
    pace_warnings,
    parent_ledger,
    phrase_findings,
    shared_run_warnings,
    spoken_lines,
    style_warnings,
    tts_problems,
)
from pipeline._lib.script import ScriptError, parse_script

REPORT_HEADER = (
    "# Written by pipeline lint. Give each warning you keep a one-line reason; the reason\n"
    "# stays as long as the warning does.\n"
)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="the repo checkout, for the phrase list, the Lexicon and the Episode registry",
    )
    parser.add_argument(
        "--pron-check",
        action="store_true",
        help="instead of linting, show what Kokoro says for each Lexicon entry in force for "
        "the Bundle, beside espeak's own reading of the term",
    )


def main(args: argparse.Namespace) -> int:
    if args.pron_check:
        return pron_check(args.bundle, args.repo)
    started = time.perf_counter()
    # A Windows console can't encode an emoji the lint is reporting; escape it, don't crash.
    sys.stdout.reconfigure(errors="backslashreplace")
    bundle = args.bundle
    phrase_list = yaml.safe_load(
        (args.repo / "config" / "deslop_rules.yaml").read_text(encoding="utf-8")
    )
    problems = bundle_problems(bundle)
    warnings = []
    # Later rules need the fields; a broken meta.yaml is already reported above.
    meta = load_meta(bundle) if not any(p.startswith("meta.yaml") for p in problems) else None
    lexicon = load_lexicon(args.repo, meta)
    texts = {
        file: (bundle / file).read_text(encoding="utf-8")
        for file in ("script.md", "ledger.md", "show_notes.md")
        if (bundle / file).is_file()
    }

    # Firm rules report a line number to fix; warnings name the Segment, so a reason kept in
    # lint_report.yaml still matches after the lines above it move.
    blockable, warnable = [], []
    if "script.md" in texts:
        script = texts["script.md"]
        problems += tts_problems(script, lexicon)
        for number, segment, line in spoken_lines(script):
            blockable.append((f"script.md line {number}", line))
            warnable.append((f"script.md, {segment}", line))
        parent = None
        if meta and meta.get("parent_episode"):
            parent = parent_ledger(bundle, args.repo, meta["parent_episode"])
            if isinstance(parent, str):
                problems.append(f"meta.yaml: {parent}")
                parent = set()
        if "ledger.md" in texts:
            problems += claim_problems(script, ledger_ids(texts["ledger.md"]), parent)
        try:
            segments = parse_script(script)
        except ScriptError:
            segments = None  # already reported by bundle_problems
        if segments:
            warnings += style_warnings(segments, meta and meta["variant"], lexicon)
            if meta:
                warnings += pace_warnings(segments, meta)
    if meta:
        listing = [(f"meta.yaml {key}", meta[key]) for key in ("title", "summary")]
        blockable += listing
        warnable += listing
    if "show_notes.md" in texts:
        blockable.append(("show_notes.md", texts["show_notes.md"]))
        warnable.append(("show_notes.md", texts["show_notes.md"]))

    problems += [
        f"{where}: phrase {phrase!r} (F9)"
        for where, phrase in phrase_findings(blockable, phrase_list["block"])
    ]
    warnings += [
        f"{where}: phrase {phrase!r}"
        for where, phrase in phrase_findings(warnable, phrase_list["warn"])
    ]
    warnings += [
        f"{where}: phrase {phrase!r}"
        for where, phrase in phrase_findings(
            [("show_notes.md", texts.get("show_notes.md", ""))], phrase_list["show_notes"]
        )
    ]

    warnings += shared_run_warnings(bundle)
    if not any(p.startswith("lint_report.yaml") for p in problems):
        write_report(bundle / "lint_report.yaml", warnings)

    # In Actions the plain lines read badly in the log, so each becomes an annotation instead.
    actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for level, messages in (("error", problems), ("warning", warnings)):
        for message in messages:
            if actions:
                print(f"::{level} title=lint {bundle.name}::{message}")
            elif level == "error":
                print(f"{bundle.name}: {message}")
            else:
                print(f"{bundle.name}: warning: {message}")
    elapsed = time.perf_counter() - started
    print(
        f"lint {bundle.name}: {len(problems)} blocking, {len(warnings)} warnings "
        f"in {elapsed:.2f} s",
        file=sys.stderr,
    )
    return 1 if problems else 0


def pron_check(bundle: Path, repo: Path) -> int:
    # Phonemes are the point here, so print them, whatever the console's own encoding.
    sys.stdout.reconfigure(encoding="utf-8")
    problems = [p for p in bundle_problems(bundle) if p.startswith("meta.yaml")]
    if problems:
        for problem in problems:
            print(f"{bundle.name}: {problem}")
        return 1
    lexicon = load_lexicon(repo, load_meta(bundle))
    for term, entry in lexicon.entries.items():
        print(
            f"{term:22} kokoro: {lexicon.kokoro_says(term):30} "
            f"espeak: {phonemize(term, 'en-gb'):30} pocket: {entry.get('pocket') or '(as written)'}"
        )
    print("verified:", " ".join(f"{w}={phonemize(w, 'en-gb')}" for w in sorted(lexicon.verified)))
    return 0


def write_report(path: Path, warnings: list[str]) -> None:
    """Record this run's warnings, keeping the reason the Skill gave for any warning it kept
    on an earlier run; a warning that has gone takes its reason with it."""
    old = yaml.safe_load(path.read_text(encoding="utf-8"))
    old_warnings = old.get("warnings") if isinstance(old, dict) else None
    reasons = {
        w["warning"]: w.get("reason")
        for w in old_warnings or []
        if isinstance(w, dict) and "warning" in w
    }
    entries = [{"warning": w, "reason": reasons.get(w)} for w in warnings]
    path.write_text(
        REPORT_HEADER
        + yaml.safe_dump({"warnings": entries}, sort_keys=False, allow_unicode=True, width=200),
        encoding="utf-8",
        newline="\n",
    )
