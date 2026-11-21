#!/usr/bin/env python3
"""Entry point for the news-image-20261121 entry.

Copies the pre-built entry image (entry/entry.png, next to this file)
to MAKEFUN_OUTPUT_DIR (default /output) as entry.png, verifies the
copy byte-for-byte with SHA-256, and leaves it world-readable (0644)
as skill.md 1.5.236 requires. Stdlib only, no network, deterministic.
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
    print("entry.png -> %s (%s, mode 0644)" % (dest, actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
