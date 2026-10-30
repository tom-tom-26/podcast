"""The Window: which Episodes' audio the Pages site holds (ticket 08)."""

import re
from pathlib import Path

PIN_LIST = "pinned.txt"
MB = 1e6


def load_pins(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def choose_window(episodes: list[dict], pins: list[str], budget: float) -> list[dict]:
    """The pinned Episodes, then the newest others while the audio is under budget, in registry
    order. Parts of a topic (4a, 4b) come and go together, so a pin on one keeps them all."""
    groups: dict[str, list[dict]] = {}
    for episode in episodes:
        groups.setdefault(_topic(episode["number"]), []).append(episode)
    newest = list(groups.values())[-1:]
    # The newest Episode stays even when pins fill the budget: it was just published, and the
    # budget is soft.
    kept = [
        group
        for group in groups.values()
        if group in newest or any(e["episode_id"] in pins for e in group)
    ]
    total = sum(e["bytes"] for group in kept for e in group)
    for group in reversed(groups.values()):
        if total >= budget:
            break
        if group not in kept:
            # A group that crosses the budget stays whole.
            kept.append(group)
            total += sum(e["bytes"] for e in group)
    window = [e for group in kept for e in group]
    return [e for e in episodes if e in window]


def _topic(number: str) -> str:
    # Parts take letters from a (4a, 4b); Q&As take them from q (7q, 7z2) and stand alone.
    part = re.fullmatch(r"(\d+)[a-p]", number)
    return part[1] if part else number
