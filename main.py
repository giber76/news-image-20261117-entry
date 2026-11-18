#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261117 (Python 3.13, stdlib only).

The front page image is drawn by draw.py (Pillow, build time only) and shipped
as entry.png beside this file. This program copies it, byte for byte, to the
output directory the grader provides, so both graded runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))
