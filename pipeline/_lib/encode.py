import json
import re
import subprocess
from pathlib import Path

# research/15: -16 LUFS integrated, -1.5 dBTP, in loudnorm's two-pass linear mode.
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"


def encode_episode(wav: Path, m4a: Path) -> None:
    """Normalise loudness and encode as 64 kbps mono AAC at 44.1 kHz."""
    measured = _measure(wav)
    second_pass = (
        f"{LOUDNORM}:linear=true"
        f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
        f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
        f":offset={measured['target_offset']}"
    )
    m4a.parent.mkdir(parents=True, exist_ok=True)
    _ffmpeg(
        "-i", str(wav),
        "-af", f"{second_pass},aresample=44100",
        "-ac", "1", "-ar", "44100", "-c:a", "aac", "-b:a", "64k",
        "-movflags", "+faststart",
        "-y", str(m4a),
    )  # fmt: skip


def duration_seconds(audio: Path) -> int:
    run = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(audio)],
        capture_output=True, text=True,
    )  # fmt: skip
    if run.returncode:
        raise RuntimeError(f"ffprobe failed on {audio}: {run.stderr.strip()[-500:]}")
    return round(float(run.stdout))


def _measure(wav: Path) -> dict[str, str]:
    stderr = _ffmpeg("-i", str(wav), "-af", f"{LOUDNORM}:print_format=json", "-f", "null", "-")
    # loudnorm prints its measurements as the last JSON object on stderr.
    return json.loads(re.findall(r"\{[^{}]*\}", stderr)[-1])


def _ffmpeg(*args: str) -> str:
    run = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True
    )
    if run.returncode:
        raise RuntimeError(f"ffmpeg failed on {args[1]}: {run.stderr.strip()[-500:]}")
    return run.stderr
