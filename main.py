#!/usr/bin/env python3
"""news-image-20261125 entry (b150 numbers variant).

Stdlib only: the grader image has no third-party packages, so this
script only copies the pre-rendered entry.png into the output dir.
"""
import os
import shutil


def main():
    """Copy the pre-rendered entry.png into the grader output dir."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    assert os.path.getsize(dst) > 0, "copied entry.png is empty"
    return dst


if __name__ == "__main__":
    print(main())
