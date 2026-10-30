import shutil
from pathlib import Path

import pytest
import yaml

SMOKE_BUNDLE = Path(__file__).parent / "fixtures" / "bundles" / "2026-10-30-smoke"


@pytest.fixture
def smoke_bundle(tmp_path):
    """A copy of the smoke Bundle that a test may break."""
    return Path(shutil.copytree(SMOKE_BUNDLE, tmp_path / SMOKE_BUNDLE.name))


def in_voice(bundle, voice):
    meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
    meta["voice"] = voice
    (bundle / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    return bundle
