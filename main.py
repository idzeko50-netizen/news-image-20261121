#!/usr/bin/env python3
"""Entry point for the news-image-20261121 entry.

Copies the pre-built entry image (entry/entry.png, next to this file)
to MAKEFUN_OUTPUT_DIR (default /output) as entry.png, verifies the
copy byte-for-byte with SHA-256, then checks it is a JPEG (magic bytes
FF D8 FF) and under the 1 MiB size cap, and leaves it world-readable
(0644) as skill.md 1.5.236 requires. Stdlib only, no network, deterministic.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry", "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


JPEG_MAGIC = b"\xff\xd8\xff"
MAX_BYTES = 1048576


def validate_output(dest):
    """Check the copied file is a JPEG under the 1 MiB cap."""
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print("output too large: %d bytes > %d byte cap" % (size, MAX_BYTES),
              file=sys.stderr)
        return 1
    with open(dest, "rb") as f:
        magic = f.read(len(JPEG_MAGIC))
    if magic != JPEG_MAGIC:
        print("output is not a JPEG: first bytes %r, expected %r"
              % (magic, JPEG_MAGIC), file=sys.stderr)
        return 1
    return 0


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    expected = sha256(SRC)
    shutil.copyfile(SRC, dest)
    os.chmod(dest, 0o644)
    actual = sha256(dest)
    if actual != expected:
        print("SHA-256 mismatch after copy: %s != %s" % (actual, expected),
              file=sys.stderr)
        return 1
    bad = validate_output(dest)
    if bad:
        return bad
    print("entry.png -> %s (%s, mode 0644)" % (dest, actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
