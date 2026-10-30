"""Render a Bundle's Script to audio, with its chunk map beside it."""

import argparse
import random
import sys
import time
import wave
from collections.abc import Callable
from pathlib import Path

import numpy as np
import yaml

from pipeline._lib.bundle import load_meta
from pipeline._lib.lexicon import load_lexicon
from pipeline._lib.pacing import draw_gap, draw_speed, load_pacing, plan_chunks
from pipeline._lib.roster import load_roster
from pipeline._lib.script import parse_script
from pipeline._lib.synthesise import RATE, kokoro_lang, synthesise


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("bundle", type=Path, help="the Bundle folder")
    parser.add_argument("--out", type=Path, help="the WAV file to write")
    parser.add_argument(
        "--voice", help="a roster voice to read the Bundle in instead of its own, for dry runs"
    )
    parser.add_argument(
        "--engine",
        action="store_true",
        help="print the engine the voice needs and render nothing, so a workflow installs it",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="the repo checkout, for the voice roster, pacing config and Lexicon",
    )


def main(args: argparse.Namespace) -> int:
    if args.engine:
        voice = args.voice or load_meta(args.bundle)["voice"]
        print(_settings(args.bundle, load_roster(args.repo), voice)["engine"])
        return 0
    if args.out is None:
        print(
            f"render {args.bundle.name}: --out is needed unless --engine is given", file=sys.stderr
        )
        return 2
    render_bundle(args.bundle, args.out, args.repo, voice=args.voice)
    return 0


def chunk_map_path(wav: Path) -> Path:
    return wav.with_suffix(".chunks.yaml")


def render_bundle(
    bundle: Path,
    wav: Path,
    repo: Path = Path("."),
    synthesise: Callable[..., np.ndarray] = synthesise,
    voice: str | None = None,
) -> None:
    """Write the Bundle's Script as a 24 kHz mono WAV, and the chunk map that names each
    chunk's Segment, text and place in the WAV."""
    started = time.perf_counter()
    meta = load_meta(bundle)
    voice = voice or meta["voice"]
    roster = load_roster(repo)
    settings = _settings(bundle, roster, voice)
    pacing = load_pacing(repo)
    say = _speaker(bundle, repo, meta, voice, settings, pacing, synthesise)
    plan = plan_chunks(
        parse_script((bundle / "script.md").read_text(encoding="utf-8")), pacing["chunk_cap"]
    )
    # Every draw is made before any audio, so a chunk's draws never depend on another's audio.
    rng = random.Random(bundle.name)
    for chunk in plan:
        chunk["gap_seconds"] = draw_gap(rng, pacing["gaps"][chunk["gap"]]) if chunk["gap"] else 0
        _draw_voice(rng, chunk, settings, pacing)
    _warn_below_floor(bundle, settings, roster.get("stretch_floor", 0))
    timeline: list[np.ndarray] = []
    at = 0
    for index, chunk in enumerate(plan):
        gap = int(RATE * chunk["gap_seconds"])
        timeline.append(np.zeros(gap, dtype=np.float32))
        audio = say(index, chunk)
        timeline.append(audio)
        chunk["start"], chunk["end"] = at + gap, at + gap + len(audio)
        at = chunk["end"]
    audio = np.concatenate(timeline)
    # start and end are sample offsets into the WAV.
    _write(wav, audio, {"bundle": bundle.name, "voice": voice, "rate": RATE, "chunks": plan})
    print(
        f"render {bundle.name}: {len(plan)} chunks, {len(audio) / RATE:.1f} s of audio "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )


def rerender_chunk(
    bundle: Path,
    wav: Path,
    index: int,
    repo: Path = Path("."),
    synthesise: Callable[..., np.ndarray] = synthesise,
) -> None:
    """Render one chunk of a rendered WAV again, for a gate that named it: Kokoro with a
    fresh speed draw, Pocket with a fresh seed. Gaps and every other chunk stay as they were."""
    started = time.perf_counter()
    meta = load_meta(bundle)
    roster = load_roster(repo)
    pacing = load_pacing(repo)
    chunk_map = yaml.safe_load(chunk_map_path(wav).read_text(encoding="utf-8"))
    # The chunk map's voice, since a dry run may have read the Bundle in another voice.
    voice = chunk_map["voice"]
    settings = _settings(bundle, roster, voice)
    chunks = chunk_map["chunks"]
    chunk = chunks[index]
    # Seeded by the retry count too, so a retry is repeatable but never the first draw again.
    chunk["retries"] = chunk.get("retries", 0) + 1
    rng = random.Random(f"{bundle.name}:{index}:{chunk['retries']}")
    # Kokoro is deterministic, so only a new speed changes its take; Pocket gets a new take
    # of the same stretch.
    if settings["engine"] == "pocket":
        chunk["seed"] = _pocket_seed(rng, settings)
    else:
        chunk["speed"] = draw_speed(rng, settings, pacing)
    say = _speaker(bundle, repo, meta, voice, settings, pacing, synthesise)
    audio = say(index, chunk)
    with wave.open(str(wav)) as old:
        samples = np.frombuffer(old.readframes(old.getnframes()), dtype="<i2") / 32767
    shift = len(audio) - (chunk["end"] - chunk["start"])
    samples = np.concatenate([samples[: chunk["start"]], audio, samples[chunk["end"] :]])
    chunk["end"] += shift
    for later in chunks[index + 1 :]:
        later["start"] += shift
        later["end"] += shift
    _write(wav, samples, chunk_map)
    print(
        f"render {bundle.name}: re-rendered chunk {index} (retry {chunk['retries']}) "
        f"in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )


def _settings(bundle: Path, roster: dict, voice: str) -> dict:
    if voice not in roster["voices"]:
        raise RuntimeError(f"render {bundle.name}: voice {voice!r} is not in the voice roster")
    return roster["voices"][voice]


def _draw_voice(rng: random.Random, chunk: dict, settings: dict, pacing: dict) -> None:
    chunk["speed"] = draw_speed(rng, settings, pacing)
    # Kokoro is deterministic and draws no seed, which leaves its gaps as they were.
    if settings["engine"] == "pocket":
        chunk["seed"] = _pocket_seed(rng, settings)


def _pocket_seed(rng: random.Random, settings: dict) -> int:
    # Pocket samples, so each chunk gets its own seed; the roster's seed re-rolls a voice.
    return rng.getrandbits(32) ^ settings.get("seed", 0)


def _warn_below_floor(bundle: Path, settings: dict, floor: float) -> None:
    stretch = settings.get("stretch")
    if stretch is not None and stretch < floor:
        print(
            f"render {bundle.name}: stretch {stretch} is below the {floor} floor; "
            "slower stretches sounded wrong in the audition",
            file=sys.stderr,
        )


def _speaker(bundle, repo, meta, voice, settings, pacing, synthesise):
    engine = settings["engine"]
    lexicon = load_lexicon(repo, meta)

    def say(index: int, chunk: dict) -> np.ndarray:
        text = chunk["text"]
        try:
            said = lexicon.apply(text, engine, kokoro_lang(voice))
            audio = synthesise(said, voice, chunk["speed"], engine, chunk.get("seed"))
            return _trim(np.asarray(audio, dtype=np.float32), pacing["trim"])
        except Exception as error:
            raise RuntimeError(
                f"render {bundle.name}: chunk {index} failed: {text[:60]!r}"
            ) from error

    return say


def _trim(audio: np.ndarray, trim: dict) -> np.ndarray:
    loud = np.flatnonzero(np.abs(audio) > trim["threshold"])
    if not len(loud):
        return audio[:0]
    pad = int(RATE * trim["pad"])
    audio = audio[max(0, loud[0] - pad) : loud[-1] + pad].copy()
    fade = min(len(audio) // 2, int(RATE * trim["fade"]))
    if fade:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        audio[:fade] *= ramp
        audio[-fade:] *= ramp[::-1]
    return audio


def _write(wav: Path, audio: np.ndarray, chunk_map: dict) -> None:
    wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(wav), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(np.round(np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    chunk_map_path(wav).write_text(
        yaml.safe_dump(chunk_map, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
