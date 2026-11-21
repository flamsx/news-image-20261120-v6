#!/usr/bin/env python3
"""Friday 20 November 2026 world-news front page (make.fun news-image-20261120 v6).

Stdlib-only entrypoint: copies the pre-rendered entry.jpg to
/output/entry.png, verifying its sha256, its size (at most 1 MiB) and its
JPEG dimensions (at most 1024 by 1024) first. The image itself was drawn
locally by draw.py (Pillow + Lexend) and is shipped as a file, so nothing
is drawn at grade time and no third-party library is needed.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.jpg")
SHA256 = "0697d3bfc539bd81c489af2e44c2de27d0894d94867395afd299b51750898c0e"
MAX_BYTES = 1048576


def jpeg_size(path):
    """Read width/height from a JPEG's SOF marker, stdlib only."""
    with open(path, "rb") as f:
        data = f.read(2)
        if data != b"\xff\xd8":
            raise ValueError("not a JPEG file")
        while True:
            marker = f.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                raise ValueError("bad JPEG marker")
            code = marker[1]
            if code in (0xD8, 0xD9) or 0xD0 <= code <= 0xD7:
                continue
            (length,) = struct.unpack(">H", f.read(2))
            if 0xC0 <= code <= 0xCF and code not in (0xC4, 0xC8, 0xCC):
                f.read(1)
                (height, width) = struct.unpack(">HH", f.read(4))
                return width, height
            f.seek(length - 2, 1)


def main():
    with open(ENTRY, "rb") as f:
        blob = f.read()
    if len(blob) > MAX_BYTES:
        raise ValueError("entry over 1 MiB: %d bytes" % len(blob))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256:
        raise ValueError("entry sha256 mismatch")
    width, height = jpeg_size(ENTRY)
    if width > 1024 or height > 1024:
        raise ValueError("entry over 1024x1024: %dx%d" % (width, height))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ENTRY, out)
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (out, width, height, len(blob), digest[:16]))


if __name__ == "__main__":
    main()
