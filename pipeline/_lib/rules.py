"""The lint's rules over a Bundle's text: firm ones block, the rest warn (spec, Pipeline > lint)."""

import re
from pathlib import Path

import yaml

from pipeline._lib.bundle import BUNDLE_ID
from pipeline._lib.lexicon import Lexicon
from pipeline._lib.registry import REGISTRY, load_registry
from pipeline._lib.script import CLAIM_TAG, PAUSE, Pause, ScriptError, Segment, parse_script

BANNED_SYMBOLS = re.compile(r"[()\[\]—–/&+%$€£…*_#@\U0001F300-\U0001FAFF\U00002600-\U000027BF]")
URL = re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(?:com|org|net|gov|edu|io|uk|co)\b", re.I)
# Dotted initials (e.g., a.m., U.S.) plus common short forms. "No." and "St." are left out:
# "No." is an everyday spoken answer.
ABBREVIATION = re.compile(
    r"\b(?:[a-z]\.){2,}"
    r"|\b(?:Dr|Mr|Mrs|Ms|Prof|vs|etc|approx|cf|et al|Jan|Feb|Aug|Sept|Oct|Nov|Dec)\.",
    re.I,
)
CONTENT_SEGMENT = re.compile(r"\d+:")
FILLER = re.compile(r"\b(?:um|uh|erm|haha)\b|\[(?:laughs?|sighs?|pause|music)\]|\*[a-z ]+\*", re.I)


def spoken_lines(script: str) -> list[tuple[int, str, str]]:
    """Script lines read aloud, as (line number, Segment title, text), markup removed."""
    lines = []
    segment = ""
    for number, line in enumerate(script.splitlines(), start=1):
        if line.startswith("## "):
            segment = line[3:].strip()
            continue
        spoken = PAUSE.sub("", CLAIM_TAG.sub("", line)).strip()
        if spoken:
            lines.append((number, segment, spoken))
    return lines


def spoken_paragraphs(segment: Segment) -> list[str]:
    return [
        " ".join(p for p in paragraph if isinstance(p, str)) for paragraph in segment.paragraphs
    ]


def phrase_findings(texts: list[tuple[str, str]], phrases: list[str]) -> list[tuple[str, str]]:
    """(where, phrase) for each listed phrase found in each (where, text)."""
    found = []
    for phrase in phrases:
        pattern = re.compile(rf"(?<!\w)(?:{phrase})(?!\w)", re.I)
        found += [(where, m[0]) for where, text in texts for m in pattern.finditer(text)]
    return found


def ledger_ids(ledger: str) -> set[str]:
    return {line.split("|", 1)[0].strip() for line in ledger.splitlines() if "|" in line}


LEDGER_FIELDS = ["id", "claim", "source", "tier", "read depth", "n and population", "tags"]
TIERS = {"1", "2", "3", "4"}
READ_DEPTHS = {"full text", "abstract", "secondary"}


def ledger_warnings(ledger: str) -> list[str]:
    """Ledger lines not in the LEDGER_FIELDS shape. The claim-check and the firm number rule
    both lean on tier and read depth, so a line missing them is worth fixing, though only a
    broken Claim tag blocks."""
    warnings = []
    for line in ledger.splitlines():
        if "|" not in line:
            continue
        fields = [field.strip() for field in line.split("|")]
        where = f"ledger.md, {fields[0]}"
        if len(fields) != len(LEDGER_FIELDS):
            warnings.append(
                f"{where}: {len(fields)} fields, not {len(LEDGER_FIELDS)} "
                f"({' | '.join(LEDGER_FIELDS)})"
            )
            continue
        if fields[3] not in TIERS:
            warnings.append(f"{where}: tier {fields[3]!r} is not 1 to 4")
        if fields[4] not in READ_DEPTHS:
            warnings.append(
                f"{where}: read depth {fields[4]!r} is not full text, abstract or secondary"
            )
    return warnings


def parent_ledger(bundle: Path, repo: Path, parent_episode: str) -> set[str] | str:
    """A Q&A parent's ledger ids, found through the Episode registry, or why it can't be read.
    The parent Bundle sits beside this one."""
    registry = repo / REGISTRY
    if not registry.is_file():
        return f"parent_episode {parent_episode}: no Episode registry at {registry}"
    for episode in load_registry(registry.read_text(encoding="utf-8")):
        if episode["episode_id"] == parent_episode:
            ledger = bundle.parent / episode["bundle_id"] / "ledger.md"
            if not ledger.is_file():
                return f"parent_episode {parent_episode}: no ledger at {ledger}"
            return ledger_ids(ledger.read_text(encoding="utf-8"))
    return f"parent_episode {parent_episode}: not in the Episode registry"


def claim_problems(script: str, ledger: set[str], parent: set[str] | None) -> list[str]:
    """Claim tags that resolve to no ledger line, and content Segments with no Claim tag.
    `{p:cN}` tags resolve against `parent`, the Q&A parent's ledger."""
    problems = []
    segment, tagged = None, False

    def end_segment() -> None:
        # Content Segments are the numbered ones, `## 1: Title` (research/05 6.3).
        if segment and CONTENT_SEGMENT.match(segment) and not tagged:
            problems.append(f"script.md, {segment}: content Segment has no Claim tag")

    for number, line in enumerate(script.splitlines(), start=1):
        if line.startswith("## "):
            end_segment()
            segment, tagged = line[3:].strip(), False
            continue
        for tag in CLAIM_TAG.findall(line):
            tagged = True
            for claim in re.findall(r"(?:p:)?c\d+", tag):
                where = f"script.md line {number}: Claim tag {claim}"
                if not claim.startswith("p:"):
                    if claim not in ledger:
                        problems.append(f"{where} has no ledger line")
                elif parent is None:
                    problems.append(f"{where} but meta.yaml has no parent_episode")
                elif claim[2:] not in parent:
                    problems.append(f"{where} has no line in the parent's ledger")
    end_segment()
    return problems


def tts_problems(script: str, lexicon: Lexicon) -> list[str]:
    """Written forms the TTS engine would read wrongly or literally (research/14). A Lexicon
    term is exempt, so CYP1A2 can stay in the Script once it has an entry."""
    problems = []
    for number, _, line in spoken_lines(script):
        where = f"script.md line {number}"
        problems += [
            f"{where}: capitals {word!r}: not verified; add a Lexicon entry or say it another way"
            for word in lexicon.unverified_capitals(line)
        ]
        line = lexicon.without_terms(line)
        problems += [
            f"{where}: digit {m[0]!r}: write it as words" for m in re.finditer(r"\d+", line)
        ]
        problems += [
            f"{where}: filler or stage direction {m[0]!r} (F5)" for m in FILLER.finditer(line)
        ]
        problems += [f"{where}: URL {m[0]!r}: not in spoken text" for m in URL.finditer(line)]
        problems += [
            f"{where}: abbreviation {m[0]!r}: write it out" for m in ABBREVIATION.finditer(line)
        ]
        problems += [
            f"{where}: symbol {s!r}: say it in words"
            for s in sorted(set(BANNED_SYMBOLS.findall(line)))
        ]
    return problems


# Soft limits warn only past research/05's number plus its 25% leniency (12.2).
LENIENCY = 1.25
SENTENCE_WORDS = 30 * LENIENCY
PARAGRAPH_SENTENCES = 5 * LENIENCY
PARAGRAPH_WORDS = 90 * LENIENCY
PER_SEGMENT = {"exclamation mark": "!", "colon": ":", "semicolon": ";"}
COUNT_ANNOUNCEMENT = re.compile(r"\bthree (?:things|ways|reasons|ideas)\b", re.I)
COUNT_ANNOUNCEMENTS = 2 * LENIENCY
# Variant ceilings in minutes (GLOSSARY, Variant); there is no minimum.
VARIANT_MINUTES = {"Quick": 15, "Standard": 28, "Deep": 35}
HOOK_WORDS = {"Quick": 120, "Standard": 150, "Deep": 150}
HETERONYMS = re.compile(
    r"\b(?:read|lead|live|close|tear|wind|minute|present|record|object|content|wound|produce"
    r"|bass|row|bow|refuse|desert)\b",
    re.I,
)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def style_warnings(segments: list[Segment], variant: str | None, lexicon: Lexicon) -> list[str]:
    """research/05 section 8's mechanical soft items, as warnings."""
    warnings = []
    titles = [segment.title for segment in segments]
    if titles[:2] != ["Hook", "Roadmap"] or titles[-2:] != ["Recap", "Sign-off"]:
        warnings.append(
            "script.md: Segments should run Hook first, then Roadmap, and end with Recap "
            "and Sign-off"
        )
    hook_words = sum(
        len(p.split()) for s in segments if s.title == "Hook" for p in spoken_paragraphs(s)
    )
    hook_limit = HOOK_WORDS.get(variant, HOOK_WORDS["Standard"])
    if hook_words > hook_limit * LENIENCY:
        warnings.append(
            f"script.md, Hook: Hook of {hook_words} words (aim for at most {hook_limit})"
        )
    announcements = 0
    for segment in segments:
        where = f"script.md, {segment.title}"
        spoken = spoken_paragraphs(segment)
        for paragraph in spoken:
            sentences = [s for s in SENTENCE_END.split(paragraph) if s]
            words = len(paragraph.split())
            if len(sentences) > PARAGRAPH_SENTENCES or words > PARAGRAPH_WORDS:
                warnings.append(
                    f"{where}: paragraph of {len(sentences)} sentences and {words} words "
                    f"(aim for at most 5 and 90)"
                )
            # No quote of the sentence: a kept reason must survive edits to its wording.
            warnings += [
                f"{where}: sentence of {len(s.split())} words (aim for at most 30)"
                for s in sentences
                if len(s.split()) > SENTENCE_WORDS
            ]
        if CONTENT_SEGMENT.match(segment.title) and not any(
            isinstance(piece, Pause) and piece.kind == "think"
            for paragraph in segment.paragraphs
            for piece in paragraph
        ):
            warnings.append(f"{where}: content Segment has no [think] for its Recall prompt")
        text = " ".join(spoken)
        for name, mark in PER_SEGMENT.items():
            if text.count(mark) > 1:
                warnings.append(f"{where}: {text.count(mark)} {name}s (aim for one a Segment)")
        warnings += [
            f"{where}: heteronym {m[0]!r}: check the reading"
            for m in HETERONYMS.finditer(lexicon.without_terms(text))
        ]
        announcements += len(COUNT_ANNOUNCEMENT.findall(text))
    if announcements > COUNT_ANNOUNCEMENTS:
        warnings.append(
            f"script.md: {announcements} 'three things' announcements (aim for at most two)"
        )
    return warnings


def pace_warnings(segments: list[Segment], meta: dict) -> list[str]:
    """Spoken words at the wpm budget, against the Variant's ceiling."""
    words = sum(
        len(paragraph.split()) for segment in segments for paragraph in spoken_paragraphs(segment)
    )
    ceiling = VARIANT_MINUTES[meta["variant"]]
    budget = meta.get("wpm_budget")
    if not isinstance(budget, int) or budget <= 0:
        return [f"meta.yaml: wpm_budget {budget!r} is not a positive number, so pace is unchecked"]
    minutes = words / budget
    if minutes > ceiling * LENIENCY:
        return [
            f"script.md: {words} words at {budget} wpm is {minutes:.0f} minutes, over the "
            f"{meta['variant']} ceiling of {ceiling}"
        ]
    return []


# The correction lines (ticket 16) are worded the same in every corrected Episode by design.
CORRECTION_NOTE = re.compile(r"^Corrected \d{4}-\d{2}-\d{2}:.*$", re.M)
SPOKEN_CORRECTION = re.compile(r"This version corrects what an earlier one said about [^.]*\.")
RUN_WORDS = 6
HISTORY = 10
FRAMING_SEGMENTS = {"Hook", "Roadmap", "Sign-off"}


def shared_run_warnings(bundle: Path) -> list[str]:
    """Six-word runs in this Bundle's framing text that one of the last ten Bundles also has,
    the template creeping in across Episodes (research/18 S13)."""
    runs = _runs(bundle)
    earlier = sorted(
        other
        for other in bundle.parent.iterdir()
        if other.is_dir() and BUNDLE_ID.fullmatch(other.name) and other.name < bundle.name
    )
    warnings = []
    for other in earlier[-HISTORY:]:
        shared = {run for _, run in _runs(other)}
        for where, run in runs:
            if run in shared:
                warnings.append(
                    f"{where}: shares the six words {' '.join(run)!r} with {other.name}"
                )
                break
    return warnings


def _runs(bundle: Path) -> list[tuple[str, tuple[str, ...]]]:
    """(where, six words) for every run in the framing text, in reading order."""
    texts = []
    if (bundle / "script.md").is_file():
        try:
            segments = parse_script((bundle / "script.md").read_text(encoding="utf-8"))
        except ScriptError:
            segments = []
        for segment in segments:
            spoken = spoken_paragraphs(segment)
            where = f"script.md, {segment.title}"
            if segment.title in FRAMING_SEGMENTS:
                texts += [(where, paragraph) for paragraph in spoken]
            elif CONTENT_SEGMENT.match(segment.title) and spoken:
                # A content Segment's signpost and question open it.
                texts.append((where, SENTENCE_END.split(spoken[0])[0]))
    if (bundle / "meta.yaml").is_file():
        try:
            meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
            texts.append(("meta.yaml summary", str(meta.get("summary") or "")))
        except (yaml.YAMLError, AttributeError):
            pass
    if (bundle / "show_notes.md").is_file():
        notes = CORRECTION_NOTE.sub("", (bundle / "show_notes.md").read_text(encoding="utf-8"))
        texts.append(("show_notes.md", notes.strip().split("\n\n")[0]))
    runs = []
    for where, text in texts:
        words = re.findall(r"[a-z']+", SPOKEN_CORRECTION.sub("", text).lower())
        runs += [
            (where, tuple(words[i : i + RUN_WORDS])) for i in range(len(words) - RUN_WORDS + 1)
        ]
    return runs
