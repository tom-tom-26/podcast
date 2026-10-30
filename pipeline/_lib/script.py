"""Script markup, research/05 6.3: `##` Segment headings, blank-line paragraphs,
`[beat]`, `[think]` and Claim tags such as `{c7}`, `{c3,c7}` or `{p:c2}`."""

import re
from dataclasses import dataclass, field

CLAIM_TAG = re.compile(r"\{\s*(?:p:)?c\d+(?:\s*,\s*(?:p:)?c\d+)*\s*\}")
PAUSE = re.compile(r"\[(beat|think)\]")


class ScriptError(ValueError):
    pass


@dataclass
class Pause:
    kind: str  # "beat" or "think"


@dataclass
class Segment:
    title: str
    # Each paragraph alternates spoken text (str) and Pauses, in Script order.
    paragraphs: list[list[str | Pause]] = field(default_factory=list)


def parse_script(text: str) -> list[Segment]:
    segments: list[Segment] = []
    paragraph: list[str] = []

    def end_paragraph() -> None:
        if paragraph:
            segments[-1].paragraphs.append(_pieces(" ".join(paragraph)))
            paragraph.clear()

    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if line.startswith("## "):
            if segments:
                end_paragraph()
            segments.append(Segment(title=line[3:].strip()))
        elif not line:
            if segments:
                end_paragraph()
        elif not segments:
            raise ScriptError(f"line {number}: text before the first Segment heading")
        else:
            paragraph.append(line)
    if not segments:
        raise ScriptError("no Segment headings")
    end_paragraph()
    return segments


def _pieces(paragraph: str) -> list[str | Pause]:
    pieces: list[str | Pause] = []
    for i, part in enumerate(PAUSE.split(CLAIM_TAG.sub("", paragraph))):
        # re.split puts the captured pause kind at every odd index.
        if i % 2:
            pieces.append(Pause(part))
        elif spoken := " ".join(part.split()):
            pieces.append(spoken)
    return pieces
