from pathlib import Path

import yaml

ROSTER = Path("config") / "voices.yaml"


def load_roster(repo: Path) -> dict:
    """The voice roster: its voices by name, the default voice and the stretch floor."""
    return yaml.safe_load((repo / ROSTER).read_text(encoding="utf-8"))


def with_credit(notes: str, roster: dict, voice: str) -> str:
    """The show notes as published: a CC BY voice's credit line goes at the end."""
    credit = roster["voices"].get(voice, {}).get("credit")
    return f"{notes.rstrip()}\n\n{credit}" if credit else notes.rstrip()
