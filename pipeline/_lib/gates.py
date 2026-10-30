"""The audio quality gates (research/15), run on the encoded Episode decoded again, so encoding
faults are caught too. Every fail is firm (owner, 2026-10-29); pace only warns."""

import difflib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

import numpy as np

from pipeline._lib.lexicon import CAPITALS, Lexicon

ASR_MODEL = "base.en"
# The probe's clean takes missed 1-3 words in a row and broken ones 8-24; 6 is about 2 s.
MISSING_RUN = 6
MISSING_AT_END = 4
SILENCE_FLOOR_DB = -50
LONGEST_SILENCE = 3.0
LOUDNESS, LOUDNESS_MARGIN = -16.0, 2.0
TRUE_PEAK = -0.5
FORMAT = {"codec_name": "aac", "channels": 1, "sample_rate": "44100"}
PACE_MARGIN = 0.25


@dataclass
class Failure:
    gate: str
    detail: str
    chunk: int | None = None


@dataclass
class Verdict:
    failures: list[Failure] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    measures: dict = field(default_factory=dict)
    asr_report: dict = field(default_factory=dict)

    def asr_failure(self) -> Failure | None:
        return next((f for f in self.failures if f.gate == "asr"), None)


def check_episode(m4a: Path, chunk_map: dict, transcript: str, lexicon: Lexicon, wpm: int):
    """Run every gate on the encoded Episode, against the chunk map render wrote."""
    verdict = Verdict()
    chunks = chunk_map["chunks"]
    rate = chunk_map["rate"]

    stream, duration = _probe(m4a)
    wrong = [
        f"{key} {stream.get(key)!r}, not {want!r}"
        for key, want in FORMAT.items()
        if stream.get(key) != want
    ]
    if wrong:
        verdict.failures.append(Failure("format", "; ".join(wrong)))

    loudness, peak = _loudness(m4a)
    verdict.measures |= {"loudness": loudness, "true_peak": peak}
    if abs(loudness - LOUDNESS) > LOUDNESS_MARGIN:
        verdict.failures.append(
            Failure(
                "loudness", f"{loudness:.1f} LUFS, outside {LOUDNESS:.0f} ±{LOUDNESS_MARGIN:.0f}"
            )
        )
    if peak > TRUE_PEAK:
        verdict.failures.append(Failure("true peak", f"{peak:.1f} dBTP, above {TRUE_PEAK}"))

    start, length = _longest_silence(m4a, duration)
    verdict.measures["longest_silence"] = length
    if length > LONGEST_SILENCE:
        # Encoder delay shifts the m4a by a few ms against the WAV, too little to matter here.
        at = sum(1 for chunk in chunks if chunk["start"] / rate <= start) - 1
        verdict.failures.append(
            Failure(
                "silence",
                f"{length:.1f} s of silence at {start:.1f} s, over {LONGEST_SILENCE:.0f} s",
                max(at, 0),
            )
        )

    script, owner = _script_words(chunks)
    heard = spoken_words(transcript)
    matched = _matched(script, heard)
    run, run_start = _longest_miss(matched)
    tail = len(matched) - len(_rstrip_false(matched))
    verdict.measures |= {"missing_run": run, "missing_at_end": tail}
    if run >= MISSING_RUN or tail >= MISSING_AT_END:
        first = run_start if run >= MISSING_RUN else len(script) - tail
        chunk = owner[first]
        what = (
            f"{run} Script words in a row missing from the transcript"
            if run >= MISSING_RUN
            else f"the last {tail} Script words missing from the transcript"
        )
        verdict.failures.append(
            Failure("asr", f"{what}, from {' '.join(script[first : first + 6])!r}", chunk)
        )
    verdict.asr_report = _asr_report(chunks, matched, lexicon, run, tail)

    pace = len(script) / (duration / 60) if duration else 0
    verdict.measures["pace"] = pace
    if abs(pace - wpm) > wpm * PACE_MARGIN:
        verdict.warnings.append(f"pace {pace:.0f} wpm against the {wpm} wpm budget")
    return verdict


def transcribe(audio: Path) -> str:
    # Decoded by ffmpeg, not faster-whisper's PyAV path: PyAV 15+ dropped an argument
    # faster-whisper 1.2.1 passes it.
    run = subprocess.run(
        ["ffmpeg", "-v", "error", "-nostdin", "-i", str(audio),
         "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, stdin=subprocess.DEVNULL,
    )  # fmt: skip
    if run.returncode:
        raise RuntimeError(f"ffmpeg failed on {audio}: {run.stderr.decode()[-500:]}")
    samples = np.frombuffer(run.stdout, dtype="<f4")
    segments, _ = _whisper().transcribe(samples, beam_size=1, language="en", vad_filter=False)
    return " ".join(segment.text for segment in segments)


@cache
def _whisper():
    from faster_whisper import WhisperModel

    # A free public-repo runner has 4 vCPUs.
    return WhisperModel(
        ASR_MODEL,
        device="cpu",
        compute_type="int8",
        cpu_threads=4,
        download_root=os.environ.get("WHISPER_MODELS"),
    )


def spoken_words(text: str) -> list[str]:
    """Words as compared: lower case, hyphens split, and the digits ASR writes said as words."""
    text = text.lower().replace("’", "'").replace("-", " ").replace("%", " percent")
    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    words = []
    for word in re.findall(r"\d+(?:\.\d+)?|[a-z']+", text):
        if word[0].isdigit():
            whole, _, decimals = word.partition(".")
            words += _number(int(whole)).split()
            if decimals:
                words += ["point", *(_number(int(d)) for d in decimals)]
        elif word.strip("'"):
            words.append(word.strip("'"))
    return words


ONES = (
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen"
).split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _number(n: int) -> str:
    # British readings, with "and" after the hundreds, since the default voice is British.
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return f"{ONES[n // 100]} hundred" + (f" and {_number(rest)}" if rest else "")
    for size, name in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= size:
            rest = n % size
            joiner = " and " if 0 < rest < 100 else " "
            return f"{_number(n // size)} {name}" + (joiner + _number(rest) if rest else "")
    raise AssertionError(n)


def _script_words(chunks: list[dict]) -> tuple[list[str], list[int]]:
    words, owner = [], []
    for index, chunk in enumerate(chunks):
        said = spoken_words(chunk["text"])
        words += said
        owner += [index] * len(said)
    return words, owner


def _matched(script: list[str], heard: list[str]) -> list[bool]:
    matched = [False] * len(script)
    blocks = difflib.SequenceMatcher(None, script, heard, autojunk=False).get_matching_blocks()
    for block in blocks:
        matched[block.a : block.a + block.size] = [True] * block.size
    return matched


def _longest_miss(matched: list[bool]) -> tuple[int, int]:
    best, best_start, run = 0, 0, 0
    for index, hit in enumerate(matched):
        run = 0 if hit else run + 1
        if run > best:
            best, best_start = run, index - run + 1
    return best, best_start


def _rstrip_false(matched: list[bool]) -> list[bool]:
    end = len(matched)
    while end and not matched[end - 1]:
        end -= 1
    return matched[:end]


def _asr_report(chunks, matched, lexicon: Lexicon, run: int, tail: int) -> dict:
    """Which capitals words and Lexicon terms the transcript heard as written: weak evidence
    the Skill weighs before it proposes a `verified:` addition, never an entry by itself."""
    terms, at = [], 0
    for index, chunk in enumerate(chunks):
        text = chunk["text"]
        found = [(m, "lexicon") for m in lexicon.terms.finditer(text)] if lexicon.terms else []
        found += [(m, "capitals") for m in CAPITALS.finditer(lexicon.without_terms(text))]
        for match, kind in sorted(found, key=lambda pair: pair[0].start()):
            first = at + len(spoken_words(text[: match.start()]))
            span = matched[first : first + len(spoken_words(match[0]))]
            terms.append(
                {"term": match[0], "kind": kind, "chunk": index, "heard": bool(span) and all(span)}
            )
        at += len(spoken_words(text))
    return {"model": ASR_MODEL, "longest_missing_run": run, "missing_at_end": tail, "terms": terms}


def _probe(m4a: Path) -> tuple[dict, float]:
    run = _run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(m4a))
    probe = json.loads(run.stdout)
    streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
    return (streams[0] if streams else {}), float(probe["format"]["duration"])


def _loudness(m4a: Path) -> tuple[float, float]:
    stderr = _ffmpeg(m4a, "ebur128=peak=true")
    # The summary comes last; the per-frame lines before it hold running values.
    summary = stderr[stderr.rindex("Summary:") :]
    loudness = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)[1])
    peak = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary)[1])
    return loudness, peak


def _longest_silence(m4a: Path, duration: float) -> tuple[float, float]:
    stderr = _ffmpeg(m4a, f"silencedetect=noise={SILENCE_FLOOR_DB}dB:d=0.5")
    longest = (0.0, 0.0)
    start = None
    for kind, value in re.findall(r"silence_(start|end): (-?[\d.]+)", stderr):
        if kind == "start":
            start = max(float(value), 0.0)
        elif start is not None:
            longest = max(longest, (start, float(value) - start), key=lambda s: s[1])
            start = None
    if start is not None:  # silence that runs to the end of the file
        longest = max(longest, (start, duration - start), key=lambda s: s[1])
    return longest


def _ffmpeg(m4a: Path, audio_filter: str) -> str:
    return _run("ffmpeg", "-hide_banner", "-nostats", "-i", str(m4a), "-af", audio_filter,
                "-f", "null", "-").stderr  # fmt: skip


def _run(*command: str) -> subprocess.CompletedProcess:
    run = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if run.returncode:
        raise RuntimeError(f"{command[0]} failed on {command[-1]}: {run.stderr.strip()[-500:]}")
    return run
