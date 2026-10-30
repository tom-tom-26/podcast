"""Chunking and the drawn gaps and speeds, from the pacing config (research/18 5.4)."""

import math
import random
import re
from pathlib import Path

import yaml

from pipeline._lib.script import Pause, Segment

PACING = Path("config") / "pacing.yaml"
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def load_pacing(repo: Path) -> dict:
    return yaml.safe_load((repo / PACING).read_text(encoding="utf-8"))


def pack(text: str, cap: int) -> list[str]:
    """The text's sentences packed into chunks of at most cap characters."""
    chunks: list[str] = []
    for sentence in SENTENCE_END.split(text):
        if chunks and len(chunks[-1]) + 1 + len(sentence) <= cap:
            chunks[-1] += " " + sentence
        else:
            chunks.append(sentence)
    return chunks


# When boundaries meet, as with a [think] closing a paragraph, the gap is the strongest one's.
STRENGTH = ["chunk", "paragraph", "beat", "segment", "think", "think_why"]


def plan_chunks(segments: list[Segment], cap: int) -> list[dict]:
    """Every chunk in Script order, with its Segment and the kind of gap before it."""
    chunks: list[dict] = []
    gap = None
    for segment in segments:
        gap = _stronger(gap, "segment")
        for paragraph in segment.paragraphs:
            gap = _stronger(gap, "paragraph")
            for piece in paragraph:
                if isinstance(piece, Pause):
                    kind = piece.kind
                    if kind == "think" and chunks and _asks_why(chunks[-1]["text"]):
                        kind = "think_why"
                    gap = _stronger(gap, kind)
                    continue
                for text in pack(piece, cap):
                    chunks.append({"segment": segment.title, "text": text, "gap": gap or "chunk"})
                    gap = None
    if chunks:
        chunks[0]["gap"] = None
    return chunks


def _stronger(gap: str | None, kind: str) -> str:
    return kind if gap is None or STRENGTH.index(kind) > STRENGTH.index(gap) else gap


def _asks_why(text: str) -> bool:
    return any(s.lower().startswith("why") and s.endswith("?") for s in SENTENCE_END.split(text))


def draw_gap(rng: random.Random, gap: dict) -> float:
    if "lognormal" in gap:
        median, factor = gap["lognormal"]
        seconds = median * math.exp(rng.gauss(0, math.log(factor)))
    else:
        seconds = rng.uniform(*gap["uniform"])
    low, high = gap["clip"]
    return min(high, max(low, seconds))
