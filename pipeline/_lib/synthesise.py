"""The TTS engine seam. Engines are imported only when used, because a workflow installs
only the engine its voice needs."""

import os
from functools import cache
from pathlib import Path

import numpy as np

RATE = 24000


class Phonemes(str):
    """Kokoro input the Lexicon has already phonemized, so Kokoro mustn't phonemize it again."""


def synthesise(text: str, voice: str) -> np.ndarray:
    """Speak text in a voice: float32 samples at 24 kHz."""
    samples, rate = _kokoro().create(
        text,
        voice=voice,
        speed=1.0,
        lang=kokoro_lang(voice),
        is_phonemes=isinstance(text, Phonemes),
    )
    if rate != RATE:
        raise RuntimeError(f"Kokoro returned {rate} Hz audio for voice {voice}, expected {RATE}")
    return samples


@cache
def _kokoro():
    from kokoro_onnx import Kokoro

    models = Path(os.environ.get("KOKORO_MODELS", "models"))
    return Kokoro(str(models / "kokoro-v1.0.int8.onnx"), str(models / "voices-v1.0.bin"))


def kokoro_lang(voice: str) -> str:
    # Kokoro voice names start with a for American English and b for British.
    return "en-gb" if voice.startswith("b") else "en-us"
