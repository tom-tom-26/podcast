import re
import wave

import numpy as np

from pipeline import render
from tests.test_lint import REPO

RATE = 24000


class FakeEngine:
    """Stands in for a TTS engine: a quiet tone, 10 ms per character of text."""

    def __init__(self):
        self.calls = []

    def __call__(self, text, voice):
        self.calls.append((text, voice))
        seconds = len(text) / 100
        return 0.1 * np.sin(np.arange(int(RATE * seconds)) * 2 * np.pi * 220 / RATE)


def render_smoke(bundle, tmp_path):
    engine = FakeEngine()
    wav = tmp_path / "out.wav"
    render.render_bundle(bundle, wav, repo=REPO, synthesise=engine)
    return engine, wav


def test_markup_is_never_spoken(smoke_bundle, tmp_path):
    engine, _ = render_smoke(smoke_bundle, tmp_path)

    spoken = " ".join(text for text, _ in engine.calls)
    assert not re.search(r"[\[\]{}#]", spoken)
    assert "Air molecules scatter short wavelengths" in spoken
    assert "Thanks for listening." in spoken


def test_bundle_voice_is_used(smoke_bundle, tmp_path):
    engine, _ = render_smoke(smoke_bundle, tmp_path)

    assert {voice for _, voice in engine.calls} == {"bm_george"}


def test_no_chunk_crosses_a_pause_paragraph_or_heading(smoke_bundle, tmp_path):
    engine, _ = render_smoke(smoke_bundle, tmp_path)

    for text, _ in engine.calls:
        assert not ("sunlight is white." in text and "So where" in text)  # [beat]
        assert not ("Have a guess." in text and "Air molecules" in text)  # [think], paragraph
        assert not ("the blue come from?" in text and "In the next minute" in text)  # heading


def test_writes_a_24_khz_mono_wav_with_the_think_pause(smoke_bundle, tmp_path):
    engine, wav = render_smoke(smoke_bundle, tmp_path)

    with wave.open(str(wav)) as audio:
        assert (audio.getframerate(), audio.getnchannels()) == (RATE, 1)
        samples = np.frombuffer(audio.readframes(audio.getnframes()), dtype=np.int16)
    speech_seconds = sum(len(text) for text, _ in engine.calls) / 100
    assert len(samples) / RATE > speech_seconds
    assert longest_silence(samples) / RATE >= 2.5


def longest_silence(samples):
    silent = np.concatenate([[False], samples == 0, [False]])
    edges = np.flatnonzero(np.diff(silent.astype(np.int8)))
    return max(np.diff(edges)[::2], default=0)
