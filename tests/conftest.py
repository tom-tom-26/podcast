import shutil
from pathlib import Path

import pytest

SMOKE_BUNDLE = Path(__file__).parent / "fixtures" / "bundles" / "2026-10-30-smoke"


@pytest.fixture
def smoke_bundle(tmp_path):
    """A copy of the smoke Bundle that a test may break."""
    return Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / SMOKE_BUNDLE.name))
