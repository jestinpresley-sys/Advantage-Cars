#!/usr/bin/env python3
"""
prep-photo.py — turn a phone photo of a car into a ready-to-paste
string for the FLEET array in advantage-cars.html.

USAGE
    python3 prep-photo.py cruze.jpg
    python3 prep-photo.py cruze.jpg --top 30

Run it from the site folder — the one containing index.html — so the
photo lands in photos/ where the page expects it.

    --top N   how far down the photo to start the crop, as a percent.
              Default 25. Raise it if the crop cuts off the roof,
              lower it if there's too much sky. Check the preview
              file it writes before pasting.

OUTPUT
    photos/<name>.jpg  the cropped, resized photo, saved straight
                       into the photos/ folder ready to reference

REQUIRES
    pip install pillow
"""

import sys, os, argparse

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow isn't installed. Run:  pip install pillow")

# Cards render at 16:9 on the fleet page. 1120px wide is plenty for
# retina screens without bloating the page.
TARGET_W, TARGET_AR, QUALITY = 1120, 16 / 9, 82
OUT_DIR = "photos"


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("photo")
    ap.add_argument("--top", type=float, default=25.0)
    ap.add_argument("-h", "--help", action="help")
    a = ap.parse_args()

    if not os.path.exists(a.photo):
        sys.exit(f"Can't find {a.photo}")

    im = Image.open(a.photo)
    if im.mode != "RGB":
        im = im.convert("RGB")

    # Strip EXIF rotation so the car isn't sideways.
    try:
        from PIL import ImageOps
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass

    W, H = im.size
    crop_h = int(W / TARGET_AR)

    if crop_h > H:
        # Photo is already wider than 16:9 — crop the sides instead.
        crop_w = int(H * TARGET_AR)
        left = (W - crop_w) // 2
        box = (left, 0, left + crop_w, H)
    else:
        top = int(H * (a.top / 100))
        top = max(0, min(top, H - crop_h))
        box = (0, top, W, top + crop_h)

    card = im.crop(box).resize(
        (TARGET_W, int(TARGET_W / TARGET_AR)), Image.LANCZOS
    )

    stem = os.path.splitext(os.path.basename(a.photo))[0]
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, stem + ".jpg")

    card.save(path, quality=QUALITY, optimize=True, progressive=True)
    kb = os.path.getsize(path) / 1024

    print(f"\n  Saved:  {path}   ({kb:.0f} KB)\n")
    print("  1. Open it. Is the whole car in frame?")
    print(f"     Roof cut off? Run again with a higher --top")
    print(f"     (currently {a.top:g}). Too much sky? Lower it.")
    print("  2. In index.html, add the entry with:")
    print(f'       photo: "{path}"\n')

    if kb > 400:
        print(f"  Note: {kb:.0f} KB is on the heavy side for one card.")
        print("  Consider dropping QUALITY in this script to 75.\n")


if __name__ == "__main__":
    main()
