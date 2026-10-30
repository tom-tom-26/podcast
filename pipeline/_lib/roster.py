from pathlib import Path

import yaml

ROSTER = Path("config") / "voices.yaml"


def load_roster(repo: Path) -> dict:
    """The voice roster's voices, by name."""
    return yaml.safe_load((repo / ROSTER).read_text(encoding="utf-8"))["voices"]
