"""Render a Bundle's Script to audio."""

import argparse
import sys
import time
import wave
from collections.abc import Callable
from pathlib import Path

import numpy as np
import yaml

from pipeline._lib.bundle import load_meta
from pipeline._lib.lexicon import load_lexicon
from pipeline._lib.script import Pause, parse_script
from pipeline._lib.synthesise import RATE, kokoro_lang, synthesise

# Fixed for now; the Pacing ticket replaces these with seeded draws.
GAP_SECONDS = {"paragraph": 0.75, "segment": 1.5, "beat": 1.0, "think": 3.0}


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument("--out", type=Path, required=True, help="the WAV file to write")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="the repo checkout, for the voice roster and the Lexicon",
    )


def main(args: argparse.Namespace) -> int:
    render_bundle(args.bundle, args.out, args.repo)
    return 0


def render_bundle(
    bundle: Path,
    wav: Path,
    repo: Path = Path("."),
    synthesise: Callable[[str, str], np.ndarray] = synthesise,
) -> None:
    """Write the Bundle's Script as a 24 kHz mono WAV, one chunk per stretch of speech."""
    started = time.perf_counter()
    meta = load_meta(bundle)
    voice = meta["voice"]
    roster = yaml.safe_load((repo / "config" / "voices.yaml").read_text(encoding="utf-8"))
    if voice not in roster["voices"]:
        raise RuntimeError(f"render {bundle.name}: voice {voice!r} is not in the voice roster")
    engine = roster["voices"][voice]["engine"]
    lexicon = load_lexicon(repo, meta.get("pronunciations"))
    segments = parse_script((bundle / "script.md").read_text(encoding="utf-8"))
    timeline: list[np.ndarray] = []
    chunks = 0
    for s, segment in enumerate(segments):
        if s:
            timeline.append(_silence("segment"))
        for p, paragraph in enumerate(segment.paragraphs):
            if p:
                timeline.append(_silence("paragraph"))
            for piece in paragraph:
                if isinstance(piece, Pause):
                    timeline.append(_silence(piece.kind))
                    continue
                try:
                    said = lexicon.apply(piece, engine, kokoro_lang(voice))
                    timeline.append(np.asarray(synthesise(said, voice), dtype=np.float32))
                except Exception as error:
                    raise RuntimeError(
                        f"render {bundle.name}: chunk {chunks} failed: {piece[:60]!r}"
                    ) from error
                chunks += 1
    audio = np.concatenate(timeline)
    wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(wav), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    print(
        f"render {bundle.name}: {chunks} chunks, {len(audio) / RATE:.1f} s of audio "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )


def _silence(kind: str) -> np.ndarray:
    return np.zeros(int(RATE * GAP_SECONDS[kind]), dtype=np.float32)
