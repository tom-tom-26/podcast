import re

import yaml

REGISTRY = "episodes.yaml"
PART_LETTERS = "abc"
QA_LETTERS = "qrstuvwxyz"
HEADER = "# The Episode registry. Only the Pipeline writes it, when it publishes an Episode.\n"


def load_registry(text: str) -> list[dict]:
    return yaml.safe_load(text)["episodes"]


def dump_registry(episodes: list[dict]) -> str:
    return HEADER + yaml.safe_dump({"episodes": episodes}, sort_keys=False, allow_unicode=True)


def next_number(episodes: list[dict]) -> int:
    # Taken from the highest number so far, not the count, so a number is never reused.
    # Parts and Q&As (4a, 7q) share their topic's number, hence only the leading digits.
    return max((int(re.match(r"\d+", e["number"])[0]) for e in episodes), default=0) + 1


class NumberingError(Exception):
    pass


def number_episodes(metas: list[dict], episodes: list[dict]) -> list[str]:
    """The Episode number each Bundle publishes as: 7 alone, 4a-4c for a group of Parts, or the
    parent's topic number plus the next Q&A letter (7q to 7z, then 7z2)."""
    if any(meta.get("parent_episode") for meta in metas):
        if len(metas) > 1:
            raise NumberingError("a Q&A publishes on its own, not in a group")
        parent = metas[0]["parent_episode"]
        found = [e["number"] for e in episodes if e["episode_id"] == parent]
        if not found:
            raise NumberingError(f"its parent {parent} is not published; publish that first")
        # A Q&A on a Part, or on another Q&A, hangs off the topic number (4q).
        topic = re.match(r"\d+", found[0])[0]
        asked = sum(bool(re.fullmatch(rf"{topic}[q-z]\d*", e["number"])) for e in episodes)
        # The eleventh Q&A is z2, the twelfth z3.
        extra = asked - len(QA_LETTERS) + 2
        letter = QA_LETTERS[asked] if asked < len(QA_LETTERS) else f"z{extra}"
        return [topic + letter]
    number = next_number(episodes)
    parts = [meta.get("part") for meta in metas]
    if not any(parts):
        if len(metas) > 1:
            raise NumberingError("only the Parts of one topic publish together")
        return [str(number)]
    if not all(parts) or len({p["series_slug"] for p in parts}) > 1:
        raise NumberingError("a group must be every Part of one topic and nothing else")
    total = parts[0]["of"]
    if sorted(p["n"] for p in parts) != list(range(1, total + 1)) or any(
        p["of"] != total for p in parts
    ):
        raise NumberingError(
            f"Parts {sorted(p['n'] for p in parts)} of {total} of topic {parts[0]['series_slug']}: "
            "every Part publishes in one group, all or nothing"
        )
    return [f"{number}{PART_LETTERS[p['n'] - 1]}" for p in parts]


def episode_id(number: str, bundle_id: str) -> str:
    topic, letters = re.fullmatch(r"(\d+)(\w*)", number).groups()
    return f"ep-{int(topic):03d}{letters}-{bundle_id.split('-', 3)[3]}"
