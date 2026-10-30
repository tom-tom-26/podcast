import argparse
import json
import re
import shutil
import subprocess
import sys
import uuid
import wave
from pathlib import Path

import numpy as np
import pytest
import yaml

from pipeline import publish
from tests.fake_github import FakeGitHub

RATE = 24000


def quiet_tone_wav(path, seconds=12):
    """Speech-like enough for loudnorm and the AAC encoder: a noisy tone at about -30 dBFS
    with gaps. A pure tone encodes far under its target bitrate, which hides the setting."""
    t = np.arange(RATE * seconds) / RATE
    noise = np.random.default_rng(0).normal(0, 0.2, t.size)
    voiced = np.sin(2 * np.pi * 200 * t) + noise
    samples = 0.03 * voiced * (np.sin(2 * np.pi * 0.5 * t) > -0.5)
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes((samples * 32767).astype("<i2").tobytes())
    return path


def run_publish(*args):
    return subprocess.run(
        [sys.executable, "-m", "pipeline", "publish", *map(str, args)],
        capture_output=True,
        text=True,
    )


def test_dry_run_encodes_a_mono_64_kbps_aac_m4a_at_minus_16_lufs(smoke_bundle, tmp_path):
    wav = quiet_tone_wav(tmp_path / "render.wav")
    out = tmp_path / "artifact"

    run = run_publish(smoke_bundle, "--wav", wav, "--dry-run", "--out-dir", out)

    assert run.returncode == 0, run.stderr
    assert [f.name for f in out.iterdir()] == ["2026-10-30-smoke.m4a"]
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
    assert release["assets"] == {"ep-001-smoke.m4a": m4a.stat().st_size}
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
    assert 11 <= entry["duration"] <= 13
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


def publish_episode(bundle, tmp_path, github, *flags):
    wav = tmp_path / "render.wav"
    if not wav.exists():
        quiet_tone_wav(wav)
    parser = argparse.ArgumentParser()
    publish.add_arguments(parser)
    args = parser.parse_args(
        [str(bundle), "--wav", str(wav), "--out-dir", str(tmp_path / "out"), *flags]
    )
    return publish.main(args, github=github)


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


def in_voice(bundle, voice):
    meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
    meta["voice"] = voice
    (bundle / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    return bundle


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
