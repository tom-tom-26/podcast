import re
from datetime import date
from pathlib import Path

import yaml

from pipeline._lib.lexicon import entry_problems
from pipeline._lib.script import ScriptError, parse_script

BUNDLE_FILES = ["script.md", "meta.yaml", "show_notes.md", "ledger.md", "lint_report.yaml"]
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
BUNDLE_ID = re.compile(rf"\d{{4}}-\d{{2}}-\d{{2}}-{SLUG.pattern}")
VARIANTS = {"Quick", "Standard", "Deep"}
TIERS = {"Harmful", "Material", "Minor"}


def bundle_problems(bundle: Path) -> list[str]:
    """The Bundle schema problems that block it, as one message each."""
    problems = []
    if not BUNDLE_ID.fullmatch(bundle.name):
        problems.append(f"folder name is not a Bundle id (<date>-<slug>): {bundle.name}")
    problems += [f"{file}: missing" for file in BUNDLE_FILES if not (bundle / file).is_file()]
    if (bundle / "meta.yaml").is_file():
        problems += [f"meta.yaml: {p}" for p in _meta_problems(bundle / "meta.yaml")]
    if (bundle / "lint_report.yaml").is_file():
        try:
            yaml.safe_load((bundle / "lint_report.yaml").read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            problems.append(f"lint_report.yaml: not valid YAML: {error}")
    if (bundle / "script.md").is_file():
        try:
            parse_script((bundle / "script.md").read_text(encoding="utf-8"))
        except ScriptError as error:
            problems.append(f"script.md: {error}")
    return problems


def load_meta(bundle: Path) -> dict:
    return yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))


def _meta_problems(path: Path) -> list[str]:
    try:
        meta = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        return [f"not valid YAML: {error}"]
    if not isinstance(meta, dict):
        return ["not a mapping of fields"]
    problems = [
        f"{key} must be non-empty text"
        for key in ("title", "summary", "voice")
        if not isinstance(meta.get(key), str) or not meta[key].strip()
    ]
    if meta.get("variant") not in VARIANTS:
        problems.append(f"variant must be one of {', '.join(sorted(VARIANTS))}")
    problems += [
        f"{key} must be a whole number from 1"
        for key in ("style_guide_version", "deslop_version")
        if not _whole_number(meta.get(key))
    ]
    problems += [f"pronunciations: {p}" for p in entry_problems(meta.get("pronunciations"))]
    problems += _part_problems(meta)
    problems += _question_problems(meta)
    revision = meta.get("revision")
    if not _whole_number(revision):
        problems.append("revision must be a whole number from 1")
    problems += _correction_problems(meta)
    return problems


def _part_problems(meta: dict) -> list[str]:
    part = meta.get("part")
    if part is None:
        return []
    # Letters a-c name the Parts, so a topic splits into 2 or 3 (ticket 01).
    if (
        not isinstance(part, dict)
        or not all(_whole_number(part.get(key)) for key in ("n", "of"))
        or not 2 <= part["of"] <= 3
        or part["n"] > part["of"]
        or not isinstance(part.get("series_slug"), str)
        or not SLUG.fullmatch(part["series_slug"])
    ):
        return ["part must be null or {n, of, series_slug} with n from 1 to of, and of 2 or 3"]
    if meta.get("parent_episode"):
        return ["parent_episode: a Q&A stands alone, so it is never a Part"]
    return []


def _question_problems(meta: dict) -> list[str]:
    questions = meta.get("questions")
    if not meta.get("parent_episode"):
        if questions:
            return ["questions: only a Q&A has them, and parent_episode is not set"]
        return []
    # The show notes quote these word for word (ticket 11), so each must be real text.
    if (
        not isinstance(questions, list)
        or not questions
        or not all(isinstance(q, str) and q.strip() for q in questions)
    ):
        return ["questions: a Q&A needs the owner's questions, word for word, as a list of text"]
    return []


def _correction_problems(meta: dict) -> list[str]:
    corrections = meta.get("corrections")
    if corrections in (None, []):
        return []
    if not isinstance(corrections, list):
        return ["corrections must be a list"]
    problems = []
    for n, correction in enumerate(corrections, 1):
        # The show-notes line quotes the date, and the owner reads claim, fix and source.
        if (
            not isinstance(correction, dict)
            or not isinstance(correction.get("date"), date)
            or correction.get("tier") not in TIERS
            or not all(
                isinstance(correction.get(key), str) and correction[key].strip()
                for key in ("claim", "fix", "source")
            )
        ):
            problems.append(
                f"corrections: entry {n} needs a date (YYYY-MM-DD), a tier of "
                f"{', '.join(sorted(TIERS))}, and claim, fix and source as text"
            )
    return problems


def _whole_number(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1
