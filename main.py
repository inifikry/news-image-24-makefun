import os
import shutil

# The image is drawn at build time (draw_frontpage.py) and shipped in the
# repository; this program only copies it, so both runs write identical bytes.
HERE = os.path.dirname(os.path.abspath(__file__))

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(out_dir, "entry.png"))
