"""The Lexicon (research/14): how each engine should say the terms it gets wrong."""

import re
from functools import cache
from pathlib import Path

import yaml

from pipeline._lib.synthesise import Phonemes

LEXICON = Path("config") / "lexicon.yaml"
CAPITALS = re.compile(r"(?<![\w-])[A-Z]{2,}s?(?![\w-])")
# Kokoro reads the whole chunk with this word standing in for each term, so the words beside
# a term keep their context: phonemized on its own, a lone "a" at the cut reads as the letter.
# It ends in a consonant because a vowel lets British linking r leak into the next word.
STAND_IN = "jukebox"
# en-gb then en-us readings; the suffix is espeak's "jukebox's".
STAND_IN_PHONEMES = re.compile(r"dʒ[ˈˌ]?uːkb(?:ɒ|ɑː)ks([ɪᵻ]z)?")


class Lexicon:
    def __init__(self, verified: list[str], entries: list[dict]):
        self.verified = set(verified)
        self.entries = {entry["term"]: entry for entry in entries}
        terms = sorted(self.entries, key=len, reverse=True)
        self.terms = (
            re.compile(r"(?<![\w-])(?:" + "|".join(map(re.escape, terms)) + r")(?![\w-])")
            if terms
            else None
        )

    def without_terms(self, text: str) -> str:
        """The text with every term blanked out, for rules that entries exempt."""
        return self.terms.sub(" ", text) if self.terms else text

    def unverified_capitals(self, text: str) -> list[str]:
        return [
            word
            for word in CAPITALS.findall(self.without_terms(text))
            if word not in self.verified and word.removesuffix("s") not in self.verified
        ]

    def apply(self, text: str, engine: str, lang: str) -> str:
        """What the engine is given for this text. An entry with no field for the engine
        leaves its term as written."""
        if not self.terms or not self.terms.search(text):
            return text
        if engine == "kokoro":
            return self._kokoro(text, lang)
        return self.terms.sub(lambda m: self.entries[m[0]].get(engine) or m[0], text)

    def kokoro_says(self, term: str, lang: str = "en-gb") -> str:
        reading = self.entries[term].get("kokoro")
        if not reading:
            return phonemize(term, lang)
        return reading.strip("/") if reading.startswith("/") else phonemize(reading, lang)

    def _kokoro(self, text: str, lang: str) -> Phonemes:
        if STAND_IN in text.lower():
            raise ValueError(f"the Lexicon's stand-in word {STAND_IN!r} is in the text")
        readings = [self.kokoro_says(m[0], lang) for m in self.terms.finditer(text)]
        phonemes = phonemize(self.terms.sub(STAND_IN, text), lang)
        if len(STAND_IN_PHONEMES.findall(phonemes)) != len(readings):
            raise ValueError(
                f"espeak changed the stand-in word, so a term went unspliced: {phonemes}"
            )
        reading = iter(readings)
        return Phonemes(
            STAND_IN_PHONEMES.sub(
                lambda m: _possessive(next(reading)) if m[1] else next(reading), phonemes
            )
        )


def load_lexicon(repo: Path, meta: dict | None) -> Lexicon:
    """The shared Lexicon, with the Bundle's own `pronunciations` winning for its Episode."""
    lexicon = yaml.safe_load((repo / LEXICON).read_text(encoding="utf-8"))
    pronunciations = (meta or {}).get("pronunciations") or []
    return Lexicon(lexicon["verified"], lexicon["entries"] + pronunciations)


def entry_problems(entries: object) -> list[str]:
    if entries is None:
        return []
    if not isinstance(entries, list):
        return ["must be a list of entries"]
    return [
        f"entry {n} needs a term"
        for n, entry in enumerate(entries, start=1)
        if not isinstance(entry, dict) or not isinstance(entry.get("term"), str)
    ]


def phonemize(text: str, lang: str) -> str:
    return _tokenizer().phonemize(text, lang)


@cache
def _tokenizer():
    # Kokoro's own tokenizer, so these phonemes are exactly what Kokoro would make itself.
    from kokoro_onnx.tokenizer import Tokenizer

    return Tokenizer()


def _possessive(phonemes: str) -> str:
    last = phonemes.rstrip("ːˈˌ")[-1:]
    if last in "szʃʒ" or phonemes.endswith(("tʃ", "dʒ")):
        return phonemes + "ɪz"
    return phonemes + ("s" if last in "ptkfθ" else "z")
