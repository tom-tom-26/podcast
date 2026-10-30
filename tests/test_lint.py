import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.conftest import SMOKE_BUNDLE

REPO = Path(__file__).parent.parent


def lint(bundle, repo=REPO):
    return subprocess.run(
        [sys.executable, "-m", "pipeline", "lint", str(bundle), "--repo", str(repo)],
        capture_output=True,
        text=True,
    )


def test_smoke_bundle_passes(smoke_bundle):
    run = lint(smoke_bundle)

    assert run.returncode == 0, run.stdout + run.stderr


@pytest.mark.parametrize(
    "file", ["script.md", "meta.yaml", "show_notes.md", "ledger.md", "lint_report.yaml"]
)
def test_missing_file_blocks(smoke_bundle, file):
    (smoke_bundle / file).unlink()

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert file in run.stdout


def break_meta(bundle, old, new):
    meta = bundle / "meta.yaml"
    text = meta.read_text(encoding="utf-8")
    assert old in text
    meta.write_text(text.replace(old, new), encoding="utf-8")


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("title: Why the sky is blue\n", "", "title"),
        ("voice: bm_george", "voice: ''", "voice"),
        ("variant: Quick", "variant: Short", "variant"),
        ("revision: 1", "revision: one", "revision"),
        ("title: Why", "title: [Why", "meta.yaml"),
    ],
)
def test_malformed_meta_blocks(smoke_bundle, old, new, message):
    break_meta(smoke_bundle, old, new)

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert message in run.stdout


def test_malformed_lint_report_blocks(smoke_bundle):
    (smoke_bundle / "lint_report.yaml").write_text("warnings: [\n", encoding="utf-8")

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert "lint_report.yaml" in run.stdout


def test_folder_not_named_by_bundle_id_blocks(smoke_bundle):
    renamed = smoke_bundle.rename(smoke_bundle.with_name("smoke"))

    run = lint(renamed)

    assert run.returncode == 1
    assert "Bundle id" in run.stdout


def test_script_without_a_segment_blocks(smoke_bundle):
    (smoke_bundle / "script.md").write_text("Just talk, no heading.\n", encoding="utf-8")

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert "script.md" in run.stdout


def edit(bundle, file, old, new):
    path = bundle / file
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


SKY_LINE = "Look up on a clear afternoon and the sky is blue."


@pytest.mark.parametrize(
    ("new", "message"),
    [
        ("Look up at 3 in the afternoon and the sky is blue.", "digit"),
        ("Look up on a clear afternoon and the sky is blue (mostly).", "symbol"),
        ("Look up on a clear afternoon and the sky is 100% blue.", "symbol"),
        ("Look up on a clear afternoon and the sky is blue \U0001f600.", "symbol"),
        ("Look up on a clear afternoon at nasa.gov/sky and the sky is blue.", "URL"),
        ("Look up at https://example.org and the sky is blue.", "URL"),
        ("Look up at noon, e.g. on a clear day, and the sky is blue.", "abbreviation"),
        ("Look up at three p.m. and the sky is blue.", "abbreviation"),
        ("Look up with Dr. Rayleigh and the sky is blue.", "abbreviation"),
        ("Um, look up on a clear afternoon and the sky is blue.", "filler"),
        ("Look up on a clear afternoon and the sky is blue. [laughs]", "filler"),
        ("Look up on a clear afternoon and the sky is blue. *sighs*", "filler"),
    ],
)
def test_written_form_in_the_script_blocks(smoke_bundle, new, message):
    edit(smoke_bundle, "script.md", SKY_LINE, new)

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert "script.md" in run.stdout
    assert message in run.stdout


def test_written_form_names_the_script_line(smoke_bundle):
    edit(smoke_bundle, "script.md", SKY_LINE, "Look up at 3 in the afternoon.")

    run = lint(smoke_bundle)

    assert "script.md line 3" in run.stdout


def test_claim_tag_without_a_ledger_line_blocks(smoke_bundle):
    edit(smoke_bundle, "script.md", "{c4}", "{c9}")

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert "c9" in run.stdout


def test_content_segment_without_a_claim_tag_blocks(smoke_bundle):
    script = smoke_bundle / "script.md"
    text = script.read_text(encoding="utf-8")
    start = text.index("## 1: Scattered light")
    end = text.index("## Recap")
    untagged = text[start:end].replace("{c2}", "").replace("{c2,c3}", "").replace("{c3}", "")
    script.write_text(text[:start] + untagged + text[end:], encoding="utf-8")

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert "1: Scattered light" in run.stdout


@pytest.mark.parametrize("version", ["style_guide_version", "deslop_version"])
def test_missing_version_blocks(smoke_bundle, version):
    break_meta(smoke_bundle, f"{version}: 1\n", "")

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert version in run.stdout


@pytest.fixture
def qa_bundle(tmp_path):
    """A repo with the smoke Bundle published as Episode 1 and a Q&A Bundle on it."""
    bundles = tmp_path / "bundles"
    shutil.copytree(REPO / "config", tmp_path / "config")
    shutil.copytree(SMOKE_BUNDLE, bundles / "2026-10-30-smoke")
    (tmp_path / "episodes.yaml").write_text(
        "episodes:\n- number: '1'\n  episode_id: ep-001-smoke\n  bundle_id: 2026-10-30-smoke\n",
        encoding="utf-8",
    )
    qa = Path(shutil.copytree(SMOKE_BUNDLE, bundles / "2026-11-02-smoke-qa"))
    edit(qa, "meta.yaml", "parent_episode: null", "parent_episode: ep-001-smoke")
    edit(qa, "script.md", "{c1}", "{p:c1}")
    return qa


def test_parent_claim_tag_resolves_against_the_parent_ledger(qa_bundle):
    run = lint(qa_bundle, repo=qa_bundle.parent.parent)

    assert run.returncode == 0, run.stdout + run.stderr


def test_parent_claim_tag_without_a_parent_ledger_line_blocks(qa_bundle):
    edit(qa_bundle, "script.md", "{p:c1}", "{p:c9}")

    run = lint(qa_bundle, repo=qa_bundle.parent.parent)

    assert run.returncode == 1
    assert "p:c9" in run.stdout


def test_parent_claim_tag_without_a_parent_episode_blocks(qa_bundle):
    edit(qa_bundle, "meta.yaml", "parent_episode: ep-001-smoke", "parent_episode: null")

    run = lint(qa_bundle, repo=qa_bundle.parent.parent)

    assert run.returncode == 1
    assert "parent_episode" in run.stdout


def test_parent_episode_missing_from_the_registry_blocks(qa_bundle):
    edit(qa_bundle, "meta.yaml", "parent_episode: ep-001-smoke", "parent_episode: ep-009-gone")

    run = lint(qa_bundle, repo=qa_bundle.parent.parent)

    assert run.returncode == 1
    assert "ep-009-gone" in run.stdout


@pytest.mark.parametrize(
    ("file", "old", "new"),
    [
        ("script.md", "In the next minute", "Let's dive in. In the next minute"),
        ("script.md", "Here is the question", "Great question. Here is the question"),
        ("script.md", "Violet scatters", "It's worth noting that violet scatters"),
        ("show_notes.md", "This is the pipeline's", "We delve into this. This is the pipeline's"),
        ("meta.yaml", "summary: A one-minute", "summary: Without further ado, a one-minute"),
    ],
)
def test_core_phrase_blocks(smoke_bundle, file, old, new):
    edit(smoke_bundle, file, old, new)

    run = lint(smoke_bundle)

    assert run.returncode == 1
    assert file in run.stdout


@pytest.mark.parametrize(
    ("file", "old", "new", "phrase"),
    [
        (
            "script.md",
            "Blue light bounces",
            "This is a pivotal point. Blue light bounces",
            "pivotal",
        ),
        ("script.md", "Short wavelengths", "Studies show short wavelengths", "studies show"),
        ("show_notes.md", "Sources", "Key takeaways: blue.\n\nSources", "key takeaways"),
        ("meta.yaml", "title: Why the sky", "title: The secret of why the sky", "secret"),
    ],
)
def test_listed_phrase_only_warns(smoke_bundle, file, old, new, phrase):
    edit(smoke_bundle, file, old, new)

    run = lint(smoke_bundle)

    assert run.returncode == 0, run.stdout + run.stderr
    assert "warning" in run.stdout
    assert phrase in run.stdout.lower()
    assert file in run.stdout


def test_phrase_list_comes_from_config(qa_bundle):
    repo = qa_bundle.parent.parent
    rules = repo / "config" / "deslop_rules.yaml"
    config = yaml.safe_load(rules.read_text(encoding="utf-8"))
    config["warn"].append("scatter(s|ed)?")
    rules.write_text(yaml.safe_dump(config), encoding="utf-8")

    run = lint(qa_bundle, repo=repo)

    assert run.returncode == 0, run.stdout + run.stderr
    assert "scatter" in run.stdout


LONG_SENTENCE = (
    "Look up on a clear afternoon in the middle of summer when the air is dry and still and "
    "there is not a single cloud anywhere over the hills or the sea or the town, and the sky "
    "is blue."
)
LONG_PARAGRAPH = " ".join(["The sky is blue."] * 7)


@pytest.mark.parametrize(
    ("file", "old", "new", "message"),
    [
        ("script.md", "So where does", "I read it once. So where does", "heteronym"),
        ("script.md", SKY_LINE, LONG_SENTENCE, "words"),
        ("script.md", SKY_LINE, LONG_PARAGRAPH, "paragraph"),
        ("script.md", "So where does", "Wow! Really! So where does", "exclamation"),
        ("script.md", "So where does", "One thing: light. Two: air. So where does", "colon"),
        (
            "script.md",
            "So where does",
            "Three things matter. Three ways in. Three reasons why. So where does",
            "three things",
        ),
        ("meta.yaml", "wpm_budget: 165", "wpm_budget: 5", "minutes"),
    ],
)
def test_soft_rule_only_warns(smoke_bundle, file, old, new, message):
    edit(smoke_bundle, file, old, new)

    run = lint(smoke_bundle)

    assert run.returncode == 0, run.stdout + run.stderr
    assert "warning" in run.stdout
    assert message in run.stdout


def make_history(bundles, ids, script="## Hook\n\nSomething else entirely, said a new way.\n"):
    for bundle_id in ids:
        (bundles / bundle_id).mkdir(parents=True)
        (bundles / bundle_id / "script.md").write_text(script, encoding="utf-8")


def test_six_words_shared_with_a_recent_bundle_only_warn(tmp_path):
    bundle = Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-10-30-smoke"))
    shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-10-01-older")

    run = lint(bundle)

    assert run.returncode == 0, run.stdout + run.stderr
    assert "2026-10-01-older" in run.stdout
    assert "look up on a clear afternoon" in run.stdout


def test_six_word_check_reads_only_the_last_ten_bundles(tmp_path):
    bundle = Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-10-30-smoke"))
    shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-09-01-oldest")
    shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-11-01-later")
    make_history(tmp_path, [f"2026-10-{day:02d}-other" for day in range(10, 20)])

    run = lint(bundle)

    assert "2026-09-01-oldest" not in run.stdout
    assert "2026-11-01-later" not in run.stdout


CORRECTION_NOTE = (
    "Corrected 2026-11-03: an earlier version said violet light scatters least. "
    "That was wrong; it scatters most (Encyclopaedia Britannica).\n\n"
)
SPOKEN_CORRECTION = "This version corrects what an earlier one said about violet light. "


def correct(bundle):
    edit(bundle, "meta.yaml", "revision: 1", "revision: 2")
    edit(
        bundle,
        "meta.yaml",
        "corrections: []",
        "corrections:\n- date: 2026-11-03\n  tier: Harmful\n  claim: c3\n"
        "  fix: violet scatters most\n  source: Encyclopaedia Britannica",
    )
    edit(bundle, "show_notes.md", "Why is the sky", CORRECTION_NOTE + "Why is the sky")
    edit(bundle, "script.md", SKY_LINE, SPOKEN_CORRECTION + SKY_LINE)


def test_correction_lines_are_accepted(tmp_path):
    bundle = Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-10-30-smoke"))
    correct(bundle)
    older = Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / "2026-10-01-older"))
    correct(older)
    (older / "script.md").write_text(
        "## Hook\n\n" + SPOKEN_CORRECTION + "Fish swim.\n", encoding="utf-8"
    )
    (older / "show_notes.md").write_text(CORRECTION_NOTE + "Fish swim.\n", encoding="utf-8")
    (older / "meta.yaml").unlink()

    run = lint(bundle)

    assert run.returncode == 0, run.stdout + run.stderr
    assert "2026-10-01-older" not in run.stdout
    assert "Corrected" not in run.stdout


def report(bundle):
    return yaml.safe_load((bundle / "lint_report.yaml").read_text(encoding="utf-8"))["warnings"]


def test_warnings_are_written_to_the_lint_report(smoke_bundle):
    edit(smoke_bundle, "script.md", "Blue light bounces", "A pivotal point. Blue light bounces")

    lint(smoke_bundle)

    pivotal = [w for w in report(smoke_bundle) if "pivotal" in w["warning"]]
    assert pivotal == [{"warning": pivotal[0]["warning"], "reason": None}]


def test_lint_report_keeps_reasons_and_drops_warnings_that_went(smoke_bundle):
    edit(smoke_bundle, "script.md", "Blue light bounces", "A pivotal point. Blue light bounces")
    lint(smoke_bundle)
    kept = report(smoke_bundle)
    for warning in kept:
        warning["reason"] = "kept on purpose"
    kept.append({"warning": "script.md, Hook: phrase 'robust'", "reason": "fixed since"})
    (smoke_bundle / "lint_report.yaml").write_text(
        yaml.safe_dump({"warnings": kept}), encoding="utf-8"
    )

    lint(smoke_bundle)

    assert {w["reason"] for w in report(smoke_bundle)} == {"kept on purpose"}
    assert all("robust" not in w["warning"] for w in report(smoke_bundle))


def test_smoke_bundle_report_is_up_to_date(smoke_bundle):
    before = report(smoke_bundle)

    lint(smoke_bundle)

    assert report(smoke_bundle) == before
    assert all(w["reason"] for w in report(smoke_bundle))


def test_actions_get_annotations(smoke_bundle):
    edit(smoke_bundle, "script.md", SKY_LINE, "Look up at 3 in the afternoon.")
    run = subprocess.run(
        [sys.executable, "-m", "pipeline", "lint", str(smoke_bundle), "--repo", str(REPO)],
        capture_output=True,
        text=True,
        env={**os.environ, "GITHUB_ACTIONS": "true"},
    )

    assert run.returncode == 1
    assert "::error title=lint 2026-10-30-smoke::script.md line 3: digit '3'" in run.stdout
    assert "::warning title=lint 2026-10-30-smoke::script.md, Roadmap: heteronym" in run.stdout
