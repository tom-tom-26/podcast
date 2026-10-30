import re

import yaml

REGISTRY = "episodes.yaml"
HEADER = "# The Episode registry. Only the Pipeline writes it, when it publishes an Episode.\n"


def load_registry(text: str) -> list[dict]:
    return yaml.safe_load(text)["episodes"]


def dump_registry(episodes: list[dict]) -> str:
    return HEADER + yaml.safe_dump({"episodes": episodes}, sort_keys=False, allow_unicode=True)


def next_number(episodes: list[dict]) -> int:
    # Taken from the highest number so far, not the count, so a number is never reused.
    # Parts and Q&As (4a, 7q) share their topic's number, hence only the leading digits.
    return max((int(re.match(r"\d+", e["number"])[0]) for e in episodes), default=0) + 1
