#!/usr/bin/env python3
"""Prepare a photo for the site: resize to 2000px on the long edge and strip all metadata.

Usage: python3 prepare.py "/path/to/photo.jpg" slug
Writes public/images/<slug>.jpg and prints the width and height to use in index.html.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

LONG_EDGE = 2000


def prepare(source, slug):
    out = Path(__file__).parent / "public" / "images" / f"{slug}.jpg"
    im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    icc = im.info.get("icc_profile")
    im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
    # Saving without the exif argument drops camera, date and location data.
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True, icc_profile=icc)
    print(f'{out.name}: width="{im.width}" height="{im.height}"')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    prepare(sys.argv[1], sys.argv[2])
