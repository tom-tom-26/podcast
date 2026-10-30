import subprocess
import sys

import pytest


@pytest.mark.parametrize("entry_point", ["lint", "render", "publish", "site", "report", "merge"])
def test_entry_point_runs_from_the_command_line(entry_point):
    run = subprocess.run(
        [sys.executable, "-m", "pipeline", entry_point, "--help"],
        capture_output=True,
        text=True,
    )

    assert run.returncode == 0, run.stderr
    assert entry_point in run.stdout
