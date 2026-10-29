import subprocess
import sys

import pytest


@pytest.mark.parametrize("entry_point", ["lint", "render", "publish", "site"])
def test_entry_point_runs_from_the_command_line(entry_point):
    run = subprocess.run(
        [sys.executable, "-m", "pipeline", entry_point, "--help"],
        capture_output=True,
        text=True,
    )

    assert run.returncode == 0, run.stderr
    assert entry_point in run.stdout


def test_unbuilt_entry_point_fails_rather_than_passing_silently():
    # A lint that exits 0 before it checks anything would wave a Bundle through.
    run = subprocess.run(
        [sys.executable, "-m", "pipeline", "lint"],
        capture_output=True,
        text=True,
    )

    assert run.returncode != 0
    assert "not built yet" in run.stderr
