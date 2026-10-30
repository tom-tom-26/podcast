import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

from pipeline import render
from tests.test_lint import REPO, lint

FIXTURES = Path(__file__).parent / "fixtures"
CASES = yaml.safe_load((FIXTURES / "pronunciation_cases.yaml").read_text(encoding="utf-8"))


def spoken(case):
    return case["spoken"]


def with_line(bundle, line, pronunciations=None):
    """The Bundle with `line` as the Hook's opening paragraph and `pronunciations` added."""
    script = bundle / "script.md"
    script.write_text(
        script.read_text(encoding="utf-8").replace("## Hook\n\n", f"## Hook\n\n{line}\n\n", 1),
        encoding="utf-8",
    )
    if pronunciations is not None:
        meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
        meta["pronunciations"] = (meta.get("pronunciations") or []) + pronunciations
        (bundle / "meta.yaml").write_text(yaml.safe_dump(meta, allow_unicode=True), "utf-8")
    return bundle


@pytest.mark.parametrize("case", CASES["cases"], ids=lambda case: case["raw"])
def test_spoken_form_of_every_case_passes_lint(smoke_bundle, case):
    run = lint(with_line(smoke_bundle, case["spoken"], CASES["bundle_pronunciations"]))

    assert run.returncode == 0, run.stdout


@pytest.mark.parametrize(
    "case", [c for c in CASES["cases"] if c["raw_blocks"]], ids=lambda case: case["raw"]
)
def test_written_form_blocks(smoke_bundle, case):
    run = lint(with_line(smoke_bundle, case["raw"]))

    assert run.returncode == 1


def test_unverified_capitals_block(smoke_bundle):
    run = lint(with_line(smoke_bundle, "The FDA approved it."))

    assert run.returncode == 1
    assert "'FDA'" in run.stdout


def test_bundle_entry_covers_capitals(smoke_bundle):
    entry = {"term": "FDA", "kokoro": "/ˈɛfdˈiːˈeɪ/", "by": "skill 2026-10-30"}

    run = lint(with_line(smoke_bundle, "The FDA approved it.", [entry]))

    assert run.returncode == 0, run.stdout


def test_verified_capitals_and_their_plurals_pass(smoke_bundle):
    run = lint(with_line(smoke_bundle, "The NHS paid for two MRIs."))

    assert run.returncode == 0, run.stdout


def test_heteronym_covered_by_an_entry_does_not_warn(smoke_bundle):
    bundle = with_line(smoke_bundle, "I read it yesterday.", CASES["bundle_pronunciations"])

    lint(bundle)

    assert "heteronym ''read''" not in (bundle / "lint_report.yaml").read_text(encoding="utf-8")


def test_pronunciation_entry_without_a_term_blocks(smoke_bundle):
    run = lint(with_line(smoke_bundle, "Hello.", [{"kokoro": "rem"}]))

    assert run.returncode == 1
    assert "pronunciations" in run.stdout


class FakeEngine:
    def __init__(self):
        self.calls = []

    def __call__(self, text, voice, speed):
        self.calls.append(text)
        return np.zeros(len(text) * 240, dtype=np.float32)


def render_cases(bundle, tmp_path, voice):
    """What the engine was given for each case's spoken form, rendered in `voice`."""
    repo = tmp_path / "repo"
    shutil.copytree(REPO / "config", repo / "config")
    roster = repo / "config" / "voices.yaml"
    voices = yaml.safe_load(roster.read_text(encoding="utf-8"))
    voices["voices"]["charles"] = {"engine": "pocket"}
    voices["voices"]["am_adam"] = {"engine": "kokoro"}
    roster.write_text(yaml.safe_dump(voices), encoding="utf-8")
    meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
    meta["voice"] = voice
    (bundle / "meta.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")
    for case in CASES["cases"]:
        with_line(bundle, case["spoken"])
    with_line(bundle, "", CASES["bundle_pronunciations"])
    engine = FakeEngine()
    render.render_bundle(bundle, tmp_path / "out.wav", repo=repo, synthesise=engine)
    return " ".join(engine.calls)


@pytest.mark.parametrize("case", [c for c in CASES["cases"] if "kokoro" in c], ids=spoken)
def test_kokoro_is_given_the_entry_phonemes(smoke_bundle, tmp_path, case):
    given = render_cases(smoke_bundle, tmp_path, "bm_george")

    assert case["kokoro"] in given


def test_kokoro_reads_a_stand_in_possessive(smoke_bundle, tmp_path):
    with_line(smoke_bundle, "The WHO's advice is short.")

    given = render_cases(smoke_bundle, tmp_path, "bm_george")

    assert "dˈʌbəljuː ˈeɪtʃ ˈəʊz ɐdvˈaɪs" in given


def test_a_lone_a_beside_a_term_is_still_read_as_a_word(smoke_bundle, tmp_path):
    with_line(smoke_bundle, "Then comes a Q and A.")

    given = render_cases(smoke_bundle, tmp_path, "bm_george")

    assert "ɐ kjˈuː ənd ˈeɪ" in given


def test_an_american_kokoro_voice_is_given_the_entry_phonemes(smoke_bundle, tmp_path):
    with_line(smoke_bundle, "The WHO's advice is short.")

    given = render_cases(smoke_bundle, tmp_path, "am_adam")

    assert "dˈʌbəljuː ˈeɪtʃ ˈəʊz" in given
    assert "kjˈuː ənd ˈeɪ" in given


def test_kokoro_gets_plain_text_where_no_term_is_said(smoke_bundle, tmp_path):
    given = render_cases(smoke_bundle, tmp_path, "bm_george")

    assert "Air molecules scatter short wavelengths" in given


@pytest.mark.parametrize("case", [c for c in CASES["cases"] if "pocket" in c], ids=spoken)
def test_pocket_is_given_the_respelling(smoke_bundle, tmp_path, case):
    given = render_cases(smoke_bundle, tmp_path, "charles")

    assert case["pocket"] in given


def test_pocket_reads_a_term_with_no_pocket_field_as_written(smoke_bundle, tmp_path):
    given = render_cases(smoke_bundle, tmp_path, "charles")

    assert "The enzyme CYP1A2 clears it." in given


def test_bundle_entry_wins_over_the_shared_lexicon(smoke_bundle, tmp_path):
    with_line(smoke_bundle, "We met Kokoro.", [{"term": "Kokoro", "kokoro": "/kˈɒkɒ/"}])

    given = render_cases(smoke_bundle, tmp_path, "bm_george")

    assert "kˈɒkɒ" in given
    assert "kˈəʊkəʊɹəʊ" not in given


def pron_check(bundle):
    return subprocess.run(
        [sys.executable, "-m", "pipeline", "lint", str(bundle), "--repo", str(REPO)]
        + ["--pron-check"],
        capture_output=True,
        encoding="utf-8",
    )


def test_pron_check_shows_an_entry_beside_espeaks_own_reading(smoke_bundle):
    run = pron_check(smoke_bundle)

    assert run.returncode == 0, run.stderr
    zeitgeber = next(line for line in run.stdout.splitlines() if line.startswith("Zeitgeber"))
    assert "tsˈaɪtɡeɪbə" in zeitgeber
    assert "zˈaɪtdʒɛbə" in zeitgeber  # espeak en-gb's "zite-jebber"
    assert "Zeit-gayber" in zeitgeber


def test_pron_check_includes_the_bundles_own_entries(smoke_bundle):
    with_line(smoke_bundle, "", CASES["bundle_pronunciations"])

    run = pron_check(smoke_bundle)

    assert any(line.startswith("read it yesterday") for line in run.stdout.splitlines())
    assert "ɹˈɛd ɪt jˈɛstədˌeɪ" in run.stdout


def test_pron_check_reports_a_broken_meta_instead_of_crashing(smoke_bundle):
    (smoke_bundle / "meta.yaml").write_text("title: [Why\n", encoding="utf-8")

    run = pron_check(smoke_bundle)

    assert run.returncode == 1
    assert "meta.yaml" in run.stdout
    assert "Traceback" not in run.stderr
