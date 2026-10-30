import subprocess
import sys

import pytest


def lint(bundle):
    return subprocess.run(
        [sys.executable, "-m", "pipeline", "lint", str(bundle)],
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
