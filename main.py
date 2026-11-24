#!/usr/bin/env python3
"""news-image-20261124 — place the finished poster at the output path.

The poster (entry.png) was drawn during the build session and is checked
into this repository next to this script. When make.fun runs the entry,
this program only has to copy that image to $MAKEFUN_OUTPUT_DIR/entry.png,
byte for byte, after confirming it really is a 1024x1024 PNG.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def read_dimensions(data: bytes) -> tuple[int, int]:
    """Pull width and height out of the PNG IHDR chunk."""
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png does not start with a PNG signature")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    if not SOURCE.is_file():
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    width, height = read_dimensions(data)
    if (width, height) != EXPECTED_SIZE:
        print("entry.png is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    # A plain copy: the same bytes go out on every run, so the two
    # runs make.fun performs always produce identical output.
    target = Path(out_dir) / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print("wrote %s (%d bytes, %dx%d)" % (target, len(data), width, height))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
