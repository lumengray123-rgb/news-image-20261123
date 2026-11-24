"""Entrypoint for the news-image-20261123 submission.

Copies the pre-rendered front page (entry.png, in this repository) to the
output location make.fun expects. The image is drawn by render.py; this
program only places it in /output.
"""
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def check_image(path):
    """Refuse anything that is not a real PNG within the 1 MiB limit."""
    with open(path, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print(f"ERROR: {path} is not a PNG file (bad magic bytes)",
              file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print(f"ERROR: {path} is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        sys.exit(1)
    return size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    size = check_image(SOURCE)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
