#!/usr/bin/env python3
"""Entry point for news-image-20261124 v2.

Copies the finished front page (entry.png, drawn by
draw_frontpage_v2.py) to /output/entry.png.

Deterministic: the same input file is copied on every run, so the two
grader runs produce byte-identical output. Stdlib only, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")


if __name__ == "__main__":
    main()
