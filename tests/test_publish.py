import json
import re
import subprocess
import sys
import wave

import numpy as np

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


def publish(*args):
    return subprocess.run(
        [sys.executable, "-m", "pipeline", "publish", *map(str, args)],
        capture_output=True,
        text=True,
    )


def test_dry_run_encodes_a_mono_64_kbps_aac_m4a_at_minus_16_lufs(smoke_bundle, tmp_path):
    wav = quiet_tone_wav(tmp_path / "render.wav")
    out = tmp_path / "artifact"

    run = publish(smoke_bundle, "--wav", wav, "--dry-run", "--out-dir", out)

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


def test_without_dry_run_it_refuses_and_writes_nothing(smoke_bundle, tmp_path):
    wav = quiet_tone_wav(tmp_path / "render.wav")
    out = tmp_path / "artifact"

    run = publish(smoke_bundle, "--wav", wav, "--out-dir", out)

    assert run.returncode == 1
    assert "not built yet" in run.stderr
    assert not out.exists()


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
