"""The TTS engine seam. Engines are imported only when used, because a workflow installs
only the engine its voice needs."""

import os
from functools import cache
from pathlib import Path

import numpy as np

RATE = 24000


class Phonemes(str):
    """Kokoro input the Lexicon has already phonemized, so Kokoro mustn't phonemize it again."""


def synthesise(
    text: str, voice: str, speed: float, engine: str = "kokoro", seed: int | None = None
) -> np.ndarray:
    """Speak text in a voice at a speed (1 is the engine's own pace): float32 samples at 24 kHz.
    The voice roster names the engine; seed is for an engine that samples (Pocket)."""
    if engine == "pocket":
        return _pocket_say(text, voice, speed, seed)
    samples, rate = _kokoro().create(
        text,
        voice=voice,
        speed=speed,
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


def _pocket_say(text: str, voice: str, speed: float, seed: int | None) -> np.ndarray:
    import torch

    if seed is None:
        raise ValueError(f"Pocket voice {voice} needs a seed, or a re-render would differ")
    model = _pocket()
    if model.sample_rate != RATE:
        raise RuntimeError(f"Pocket gives {model.sample_rate} Hz audio, expected {RATE}")
    # The voice state is built first: building it the first time draws from the generator
    # the seed sets, so the first chunk would otherwise never repeat.
    state = _pocket_voice(voice)
    torch.manual_seed(seed)
    with torch.no_grad():
        audio = model.generate_audio(state, text).numpy().squeeze()
    audio = audio.astype(np.float32)
    # Pocket has no speed control, so pace comes from a time-stretch that keeps pitch.
    return audio if speed == 1 else _stretch(audio, speed)


@cache
def _pocket():
    from pocket_tts import TTSModel

    return TTSModel.load_model()


@cache
def _pocket_voice(voice: str):
    return _pocket().get_state_for_audio_prompt(voice)


def _stretch(audio: np.ndarray, speed: float) -> np.ndarray:
    from audiotsm import wsola
    from audiotsm.io.array import ArrayReader, ArrayWriter

    out = ArrayWriter(channels=1)
    wsola(channels=1, speed=speed).run(ArrayReader(audio[None, :]), out)
    return out.data[0].astype(np.float32)
