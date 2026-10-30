import argparse
import json
import re
import shutil
import subprocess
import uuid
import wave
from pathlib import Path

import numpy as np
import pytest
import yaml

from pipeline import publish, render
from tests.conftest import in_voice
from tests.fake_github import FakeGitHub
from tests.test_lint import REPO

RATE = 24000


class SpeechlikeEngine:
    """Stands in for a TTS engine with speech-like enough audio for loudnorm and the AAC
    encoder: a noisy tone at about -30 dBFS, 60 ms per character. A pure tone encodes far
    under its target bitrate, which hides the setting."""

    def __init__(self):
        self.calls = []

    def __call__(self, text, voice, speed, engine, seed):
        self.calls.append(text)
        t = np.arange(int(RATE * len(text) * 0.06)) / RATE
        noise = np.random.default_rng(len(self.calls)).normal(0, 0.2, t.size)
        voiced = np.sin(2 * np.pi * 200 * t) + noise
        return 0.03 * voiced * (np.sin(2 * np.pi * 2 * t) > -0.7)


def heard_as_written(wav, drop=None):
    """A fake transcriber that hears the rendered text, less any words named in drop:
    {chunk index: (first word, word count)}."""

    def transcribe(m4a):
        chunk_map = yaml.safe_load(render.chunk_map_path(wav).read_text(encoding="utf-8"))
        words = []
        for index, chunk in enumerate(chunk_map["chunks"]):
            said = chunk["text"].split()
            if drop and index in drop:
                first, count = drop[index]
                del said[first : first + count]
            words += said
        return " ".join(words)

    return transcribe


def test_dry_run_encodes_a_mono_64_kbps_aac_m4a_at_minus_16_lufs(smoke_bundle, tmp_path):
    assert publish_episode(smoke_bundle, tmp_path, None, "--dry-run") == 0

    out = tmp_path / "out"
    assert sorted(f.name for f in out.iterdir()) == ["2026-10-30-smoke.m4a", "asr_report.yaml"]
    m4a = out / "2026-10-30-smoke.m4a"
    probe = ffprobe(m4a)
    stream = probe["streams"][0]
    assert stream["codec_name"] == "aac"
    assert stream["channels"] == 1
    assert stream["sample_rate"] == "44100"
    # ffmpeg's AAC encoder only roughly meets its target (this signal lands anywhere from
    # 25% under to 30% over), so the range only tells 64k apart from 32k or 128k.
    assert 40_000 <= int(stream["bit_rate"]) <= 96_000
    assert "m4a" in probe["format"]["format_name"]
    assert abs(integrated_loudness(m4a) + 16) <= 1


def test_dry_run_touches_nothing_on_github(smoke_bundle, tmp_path):
    github = FakeGitHub()

    assert publish_episode(smoke_bundle, tmp_path, github, "--dry-run") == 0

    assert github.calls == []


def test_first_publish_makes_episode_1_as_a_release_and_a_registry_entry(smoke_bundle, tmp_path):
    github = FakeGitHub()

    assert publish_episode(smoke_bundle, tmp_path, github) == 0

    m4a = tmp_path / "out" / "ep-001-smoke.m4a"
    release = github.releases["ep-001-smoke"]
    assert not release["draft"]
    assert release["title"] == "Episode 1: Why the sky is blue"
    assert release["notes"].startswith("Why is the sky blue when sunlight is white?")
    assert "Encyclopaedia Britannica" in release["notes"]
    assert release["assets"] == {
        "ep-001-smoke.m4a": m4a.stat().st_size,
        "asr_report.yaml": (tmp_path / "out" / "asr_report.yaml").stat().st_size,
    }
    [entry] = registry(github)
    assert entry == {
        "number": "1",
        "episode_id": "ep-001-smoke",
        "bundle_id": "2026-10-30-smoke",
        "guid": entry["guid"],
        "voice": "bm_george",
        "file": "ep-001-smoke.m4a",
        "bytes": m4a.stat().st_size,
        "duration": entry["duration"],
    }
    assert uuid.UUID(entry["guid"])
    assert entry["duration"] == round(float(ffprobe(m4a)["format"]["duration"]))
    assert [path for path, _ in github.commits] == ["episodes.yaml"]


def test_the_upload_size_is_checked_before_the_release_goes_public_or_the_registry_changes(
    smoke_bundle, tmp_path
):
    github = FakeGitHub()

    publish_episode(smoke_bundle, tmp_path, github)

    assert github.calls == [
        "read_file",
        "create_release",
        "upload_asset",
        "upload_asset",
        "asset_sizes",
        "publish_release",
        "commit_file",
    ]


def test_numbers_count_up_in_publish_order_and_earlier_entries_never_change(smoke_bundle, tmp_path):
    github = FakeGitHub()
    publish_episode(smoke_bundle, tmp_path, github)
    [first] = registry(github)
    tides = another_bundle(smoke_bundle, "2026-11-02-tides", "How tides work")

    assert publish_episode(tides, tmp_path, github) == 0

    assert registry(github)[0] == first
    second = registry(github)[1]
    assert (second["number"], second["episode_id"]) == ("2", "ep-002-tides")
    assert second["guid"] != first["guid"]
    assert github.releases["ep-002-tides"]["title"] == "Episode 2: How tides work"


def test_a_bundle_already_published_is_refused(smoke_bundle, tmp_path, capsys):
    github = FakeGitHub()
    publish_episode(smoke_bundle, tmp_path, github)

    assert publish_episode(smoke_bundle, tmp_path, github) == 1

    assert "already published as ep-001-smoke" in capsys.readouterr().err
    assert list(github.releases) == ["ep-001-smoke"]
    assert len(registry(github)) == 1


def test_a_byte_size_mismatch_fails_with_no_registry_commit(smoke_bundle, tmp_path, capsys):
    github = FakeGitHub(upload_loses_bytes=1)

    assert publish_episode(smoke_bundle, tmp_path, github) == 1

    assert "ep-001-smoke.m4a" in capsys.readouterr().err
    assert github.releases["ep-001-smoke"]["draft"]
    assert github.commits == []
    assert registry(github) == []


def test_a_folder_that_is_not_a_bundle_id_is_refused(smoke_bundle, tmp_path, capsys):
    github = FakeGitHub()
    renamed = smoke_bundle.rename(smoke_bundle.parent / "smoke")

    assert publish_episode(renamed, tmp_path, github) == 1

    assert "not a Bundle id" in capsys.readouterr().err
    assert github.calls == []


def publish_episode(bundle, tmp_path, github, *flags, transcribe=None, encode=None, engine=None):
    """Render the Bundle with a fake engine, unless a test already rendered it, and publish it
    with the fakes given. The transcriber defaults to one that hears every word."""
    wav = tmp_path / "render.wav"
    engine = engine or SpeechlikeEngine()
    if not wav.exists():
        render.render_bundle(bundle, wav, repo=REPO, synthesise=engine)
    parser = argparse.ArgumentParser()
    publish.add_arguments(parser)
    args = parser.parse_args(
        [
            str(bundle),
            "--wav",
            str(wav),
            "--out-dir",
            str(tmp_path / "out"),
            "--repo",
            str(REPO),
            *flags,
        ]
    )
    fakes = {"transcribe": transcribe or heard_as_written(wav), "synthesise": engine}
    if encode:
        fakes["encode"] = encode
    return publish.main(args, github=github, **fakes)


def registry(github):
    return yaml.safe_load(github.files["episodes.yaml"])["episodes"]


def another_bundle(bundle, bundle_id, title):
    other = Path(shutil.copytree(bundle, bundle.parent / bundle_id))
    meta = yaml.safe_load((other / "meta.yaml").read_text(encoding="utf-8"))
    meta["title"] = title
    (other / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    return other


def ffprobe(path):
    run = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(run.stdout)


def integrated_loudness(path):
    run = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run.stderr)[-1])


@pytest.mark.parametrize(
    "voice, credit",
    [
        ("alba", "Voice: alba (Alba MacKenna), Kyutai Pocket TTS voices, CC BY 4.0"),
        ("charles", "Voice: charles (VCTK corpus, CSTR, University of Edinburgh)"),
    ],
)
def test_a_cc_by_voice_ends_the_release_text_with_its_credit_line(
    smoke_bundle, tmp_path, voice, credit
):
    github = FakeGitHub()

    assert publish_episode(in_voice(smoke_bundle, voice), tmp_path, github) == 0

    last = github.releases["ep-001-smoke"]["notes"].rstrip().split("\n\n")[-1]
    assert last.startswith(credit)
    assert last.endswith("(https://huggingface.co/kyutai/tts-voices)")


@pytest.mark.parametrize("voice", ["bm_george", "bm_lewis", "stuart_bell"])
def test_a_kokoro_or_cc0_voice_gets_no_credit_line(smoke_bundle, tmp_path, voice):
    github = FakeGitHub()

    assert publish_episode(in_voice(smoke_bundle, voice), tmp_path, github) == 0

    assert "Voice:" not in github.releases["ep-001-smoke"]["notes"]


def chunk_index(tmp_path, phrase):
    chunk_map = yaml.safe_load((tmp_path / "render.chunks.yaml").read_text(encoding="utf-8"))
    return next(i for i, c in enumerate(chunk_map["chunks"]) if phrase in c["text"])


def render_take(bundle, tmp_path, engine=None):
    engine = engine or SpeechlikeEngine()
    render.render_bundle(bundle, tmp_path / "render.wav", repo=REPO, synthesise=engine)
    return engine


def test_dropped_words_fail_the_asr_gate_naming_the_chunk_after_one_retry(
    smoke_bundle, tmp_path, capsys
):
    engine = render_take(smoke_bundle, tmp_path)
    chunk = chunk_index(tmp_path, "Air molecules")
    github = FakeGitHub()
    rendered = len(engine.calls)

    transcribe = heard_as_written(tmp_path / "render.wav", drop={chunk: (2, 8)})
    code = publish_episode(smoke_bundle, tmp_path, github, transcribe=transcribe, engine=engine)

    assert code == 1
    err = capsys.readouterr().err
    assert err.count(f"asr gate failed at chunk {chunk} (1: Scattered light: 'Air molecules") == 2
    assert err.count("re-rendering chunk") == 1
    assert engine.calls[rendered:] == [engine.calls[chunk]]
    assert github.calls == ["read_file"]


def test_a_truncated_end_fails_the_asr_gate(smoke_bundle, tmp_path, capsys):
    render_take(smoke_bundle, tmp_path)
    last = chunk_index(tmp_path, "Thanks for listening")
    github = FakeGitHub()

    transcribe = heard_as_written(tmp_path / "render.wav", drop={last: (3, 5)})
    assert publish_episode(smoke_bundle, tmp_path, github, transcribe=transcribe) == 1

    err = capsys.readouterr().err
    assert f"asr gate failed at chunk {last} (Sign-off:" in err
    assert "the last 5 Script words missing" in err
    assert github.calls == ["read_file"]


def test_a_chunk_retry_that_fixes_the_take_publishes(smoke_bundle, tmp_path, capsys):
    engine = render_take(smoke_bundle, tmp_path)
    chunk = chunk_index(tmp_path, "Air molecules")
    broken = heard_as_written(tmp_path / "render.wav", drop={chunk: (2, 8)})
    clean = heard_as_written(tmp_path / "render.wav")
    takes = iter([broken, clean])
    github = FakeGitHub()

    code = publish_episode(
        smoke_bundle, tmp_path, github, transcribe=lambda m4a: next(takes)(m4a), engine=engine
    )

    assert code == 0, capsys.readouterr().err
    assert capsys.readouterr().err.count("re-rendering chunk") == 1
    assert not github.releases["ep-001-smoke"]["draft"]


def test_four_seconds_of_silence_fails_the_silence_gate(smoke_bundle, tmp_path, capsys):
    render_take(smoke_bundle, tmp_path)
    wav = tmp_path / "render.wav"
    rate, samples = read_wav(wav)
    middle = len(samples) // 2
    write_wav(wav, np.concatenate([samples[:middle], np.zeros(4 * rate), samples[middle:]]))
    github = FakeGitHub()

    assert publish_episode(smoke_bundle, tmp_path, github, "--dry-run") == 1

    err = capsys.readouterr().err
    assert re.search(r"silence gate failed at chunk \d+ .*: 4\.\d s of silence", err)
    assert "re-rendering" not in err
    assert not (tmp_path / "out" / "asr_report.yaml").exists()


def ffmpeg_encoder(audio_filter, *settings):
    """A fake encoder that writes the faulty .m4a a broken encode step might. Plain gain, not
    loudnorm: a one-pass loudnorm hung some ffmpeg builds on this take."""

    def encode(wav, m4a):
        m4a.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-nostdin", "-i", str(wav), "-af", audio_filter,
             *(settings or ("-ac", "1", "-ar", "44100")), "-c:a", "aac", "-b:a", "64k",
             "-y", str(m4a)],
            check=True,
        )  # fmt: skip

    return encode


@pytest.mark.parametrize(
    "encode, gate",
    [
        (ffmpeg_encoder("volume=-20dB"), "loudness gate failed: -"),
        (ffmpeg_encoder("volume=30dB"), "true peak gate failed: "),
        (
            ffmpeg_encoder("volume=12dB", "-ac", "2", "-ar", "44100"),
            "format gate failed: channels 2",
        ),
        (
            ffmpeg_encoder("volume=12dB", "-ac", "1", "-ar", "24000"),
            "format gate failed: sample_rate '24000'",
        ),
    ],
    ids=["too quiet", "clipped peak", "stereo", "24 kHz"],
)
def test_a_faulty_encode_fails_the_right_gate_before_any_release(
    smoke_bundle, tmp_path, capsys, encode, gate
):
    github = FakeGitHub()

    assert publish_episode(smoke_bundle, tmp_path, github, encode=encode) == 1

    err = capsys.readouterr().err
    assert gate in err
    assert "asr gate" not in err
    assert github.calls == ["read_file"]


def test_the_clean_take_passes_every_gate(smoke_bundle, tmp_path, capsys):
    assert publish_episode(smoke_bundle, tmp_path, None, "--dry-run") == 0

    err = capsys.readouterr().err
    assert "gate failed" not in err
    assert "gates passed" in err


def test_pace_against_word_count_only_warns(smoke_bundle, tmp_path, capsys):
    meta = yaml.safe_load((smoke_bundle / "meta.yaml").read_text(encoding="utf-8"))
    meta["wpm_budget"] = 20
    (smoke_bundle / "meta.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")

    assert publish_episode(smoke_bundle, tmp_path, None, "--dry-run") == 0

    assert "against the 20 wpm budget; a warning only" in capsys.readouterr().err


def test_the_asr_report_says_which_capitals_words_and_lexicon_terms_were_heard(
    smoke_bundle, tmp_path
):
    script = smoke_bundle / "script.md"
    text = script.read_text(encoding="utf-8")
    script.write_text(
        text.replace("Thanks for listening.", "NASA and the WHO agree. Thanks for listening."),
        encoding="utf-8",
    )
    render_take(smoke_bundle, tmp_path)
    wav = tmp_path / "render.wav"

    def transcribe(m4a):
        return heard_as_written(wav)(m4a).replace("WHO", "who ho")

    github = FakeGitHub()
    assert publish_episode(smoke_bundle, tmp_path, github, transcribe=transcribe) == 0

    report = yaml.safe_load((tmp_path / "out" / "asr_report.yaml").read_text(encoding="utf-8"))
    chunk = chunk_index(tmp_path, "NASA")
    assert report["episode"] == "ep-001-smoke"
    assert report["terms"] == [
        {"term": "NASA", "kind": "capitals", "chunk": chunk, "heard": True},
        {"term": "WHO", "kind": "lexicon", "chunk": chunk, "heard": True},
    ]


def read_wav(path):
    with wave.open(str(path)) as audio:
        rate = audio.getframerate()
        return rate, np.frombuffer(audio.readframes(audio.getnframes()), dtype="<i2")


def write_wav(path, samples):
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(samples.astype("<i2").tobytes())


def test_an_asr_fail_beside_a_whole_file_fail_stops_without_a_re_render(
    smoke_bundle, tmp_path, capsys
):
    engine = render_take(smoke_bundle, tmp_path)
    chunk = chunk_index(tmp_path, "Air molecules")
    rendered = len(engine.calls)

    transcribe = heard_as_written(tmp_path / "render.wav", drop={chunk: (2, 8)})
    code = publish_episode(
        smoke_bundle, tmp_path, FakeGitHub(), transcribe=transcribe, engine=engine,
        encode=ffmpeg_encoder("volume=-20dB"),
    )  # fmt: skip

    assert code == 1
    err = capsys.readouterr().err
    assert "asr gate failed" in err and "loudness gate failed" in err
    assert "re-rendering" not in err
    assert len(engine.calls) == rendered
