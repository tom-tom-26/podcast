from pathlib import Path

import pytest
from PIL import Image

from pipeline.site import cover_problems

COVER = Path(__file__).parents[1] / "artwork" / "cover.png"


def test_committed_cover_meets_apples_rules():
    assert cover_problems(COVER) == []


@pytest.mark.parametrize(
    "mode, size, save_options, expected",
    [
        ("RGBA", (3000, 3000), {}, "colour type 6"),
        ("LA", (3000, 3000), {}, "colour type 4"),
        ("P", (3000, 3000), {}, "colour type 3"),
        ("RGB", (3000, 3000), {"transparency": (0, 0, 0)}, "tRNS"),
        ("RGB", (3000, 2000), {}, "3000x2000 is not square"),
        ("RGB", (1400, 1400), {}, "1400x1400, expected 3000x3000"),
    ],
)
def test_cover_that_breaks_a_rule_is_refused(tmp_path, mode, size, save_options, expected):
    png = tmp_path / "cover.png"
    Image.new(mode, size).save(png, **save_options)

    [problem] = cover_problems(png)

    assert expected in problem


def test_cover_that_is_not_a_png_is_refused(tmp_path):
    jpg = tmp_path / "cover.png"
    Image.new("RGB", (3000, 3000)).save(jpg, format="JPEG")

    assert cover_problems(jpg) == ["cover.png: not a PNG"]
