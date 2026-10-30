import re
import wave

import numpy as np
import yaml

from pipeline import render
from tests.conftest import SMOKE_BUNDLE
from tests.test_lint import REPO

RATE = 24000
PACING = yaml.safe_load((REPO / "config" / "pacing.yaml").read_text(encoding="utf-8"))


class FakeEngine:
    """Stands in for a TTS engine: a quiet tone that never touches zero, 10 ms per character."""

    def __init__(self):
        self.calls = []
        self.speeds = []

    def __call__(self, text, voice, speed):
        self.calls.append((text, voice))
        self.speeds.append(speed)
        seconds = len(text) / 100
        return 0.1 + 0.05 * np.sin(np.arange(int(RATE * seconds)) * 2 * np.pi * 220 / RATE)


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
    return max(silences(samples), default=0)


def test_sentences_in_a_paragraph_share_a_chunk_up_to_the_cap(smoke_bundle, tmp_path):
    sentence = "Each of these sentences is long enough to fill some of a chunk on its own."
    script = smoke_bundle / "script.md"
    script.write_text(
        script.read_text(encoding="utf-8") + "\n## Long\n\n" + " ".join([sentence] * 12) + "\n",
        encoding="utf-8",
    )

    engine, _ = render_smoke(smoke_bundle, tmp_path)

    texts = [text for text, _ in engine.calls]
    assert any("long ones. Blue light" in text for text in texts)
    long = [text for text in texts if sentence in text]
    assert sum(text.count(sentence) for text in long) == 12
    assert len(long) < 12
    assert all(len(text) <= PACING["chunk_cap"] for text in long)


def test_gaps_between_chunks_vary(smoke_bundle, tmp_path):
    _, wav = render_smoke(smoke_bundle, tmp_path)

    gaps = silences(read_samples(wav))
    assert len(gaps) >= 6
    assert len(set(gaps)) > len(gaps) // 2


def test_the_same_bundle_id_renders_byte_identical_timing(smoke_bundle, tmp_path):
    _, first = render_smoke(smoke_bundle, tmp_path / "first")
    _, second = render_smoke(smoke_bundle, tmp_path / "second")

    assert first.read_bytes() == second.read_bytes()
    assert chunk_map(first).read_bytes() == chunk_map(second).read_bytes()


def test_a_different_bundle_id_renders_different_timing(smoke_bundle, tmp_path):
    other = smoke_bundle.rename(smoke_bundle.with_name("2026-10-31-smoke"))
    _, first = render_smoke(SMOKE_BUNDLE, tmp_path / "first")
    _, second = render_smoke(other, tmp_path / "second")

    assert silences(read_samples(first)) != silences(read_samples(second))


def read_samples(wav):
    with wave.open(str(wav)) as audio:
        return np.frombuffer(audio.readframes(audio.getnframes()), dtype=np.int16)


def silences(samples):
    """The length in samples of every run of silence."""
    silent = np.concatenate([[False], samples == 0, [False]])
    edges = np.flatnonzero(np.diff(silent.astype(np.int8)))
    return list(np.diff(edges)[::2])


def chunk_map(wav):
    return render.chunk_map_path(wav)


def test_each_chunk_gets_the_voice_base_speed_with_a_little_jitter(smoke_bundle, tmp_path):
    base = yaml.safe_load((REPO / "config" / "voices.yaml").read_text(encoding="utf-8"))
    base = base["voices"]["bm_george"]["speed"]

    engine, _ = render_smoke(smoke_bundle, tmp_path)

    assert all(abs(speed - base) <= PACING["speed_jitter"] for speed in engine.speeds)
    assert len(set(engine.speeds)) == len(engine.speeds)


class PaddedEngine(FakeEngine):
    """A fake engine that, like a real one, leaves half a second of silence at each end."""

    def __call__(self, text, voice, speed):
        pad = np.zeros(RATE // 2)
        return np.concatenate([pad, super().__call__(text, voice, speed), pad])


def test_engine_silence_at_chunk_edges_is_trimmed(smoke_bundle, tmp_path):
    _, plain = render_smoke(smoke_bundle, tmp_path / "plain")
    padded = tmp_path / "padded.wav"
    engine = PaddedEngine()
    render.render_bundle(smoke_bundle, padded, repo=REPO, synthesise=engine)

    added = len(read_samples(padded)) - len(read_samples(plain))
    assert added <= len(engine.calls) * RATE * 0.05


def test_the_chunk_map_names_each_chunk_its_segment_and_place_in_the_wav(smoke_bundle, tmp_path):
    engine, wav = render_smoke(smoke_bundle, tmp_path)

    chunks = yaml.safe_load(chunk_map(wav).read_text(encoding="utf-8"))["chunks"]
    samples = read_samples(wav)
    assert len(chunks) == len(engine.calls)
    assert chunks[0]["segment"] == "Hook"
    assert chunks[-1]["segment"] == "Sign-off"
    assert chunks[-1]["text"] == "That's the sky, plainly put. Thanks for listening."
    for before, chunk in zip([{"end": 0}] + chunks, chunks, strict=False):
        assert not samples[before["end"] : chunk["start"]].any()
        assert samples[chunk["start"] + RATE // 100 : chunk["end"] - RATE // 100].all()


def test_one_chunk_re_renders_with_a_fresh_speed_and_the_rest_untouched(smoke_bundle, tmp_path):
    _, wav = render_smoke(smoke_bundle, tmp_path)
    before = yaml.safe_load(chunk_map(wav).read_text(encoding="utf-8"))["chunks"]
    old = read_samples(wav)
    engine = FakeEngine()

    render.rerender_chunk(smoke_bundle, wav, 4, repo=REPO, synthesise=engine)

    after = yaml.safe_load(chunk_map(wav).read_text(encoding="utf-8"))["chunks"]
    new = read_samples(wav)
    assert engine.calls == [(before[4]["text"], "bm_george")]
    assert after[4]["speed"] != before[4]["speed"]
    assert (new[: after[4]["start"]] == old[: before[4]["start"]]).all()
    assert (new[after[5]["start"] :] == old[before[5]["start"] :]).all()
    for b, a in zip(before, after, strict=True):
        assert a["end"] - a["start"] == b["end"] - b["start"] or a is after[4]


def think_pause_after(bundle, tmp_path, paragraph):
    (bundle / "script.md").write_text(
        f"## Hook\n\n{paragraph} [think] Now the answer.\n", encoding="utf-8"
    )
    _, wav = render_smoke(bundle, tmp_path)
    return max(silences(read_samples(wav))) / RATE


def test_a_why_question_gets_a_longer_think_pause(smoke_bundle, tmp_path):
    assert think_pause_after(smoke_bundle, tmp_path, 'So why does ice float?"') >= 4.2


def test_a_one_fact_question_after_an_earlier_why_gets_the_short_think(smoke_bundle, tmp_path):
    paragraph = "Why do people guess wrong? Here is a simpler one. What colour is grass?"
    assert think_pause_after(smoke_bundle, tmp_path, paragraph) <= 3.4
