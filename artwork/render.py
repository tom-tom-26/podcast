"""Render cover.svg to cover.png, the show's cover in the Feed.

pip install -e ".[artwork]"
python artwork/render.py
"""

import io
from pathlib import Path

import resvg_py
from PIL import Image

HERE = Path(__file__).parent


def main() -> None:
    png = resvg_py.svg_to_bytes(
        svg_path=str(HERE / "cover.svg"),
        font_files=[str(font) for font in sorted((HERE / "fonts").glob("*.ttf"))],
        # A cover that only renders on one machine's fonts can't be reproduced.
        skip_system_fonts=True,
    )
    # resvg always writes RGBA, and Apple rejects a cover with an alpha channel.
    Image.open(io.BytesIO(png)).convert("RGB").save(HERE / "cover.png", optimize=True)


if __name__ == "__main__":
    main()
