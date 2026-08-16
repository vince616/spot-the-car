import json, os
from PIL import Image, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")
OUT = os.path.join(BASE, "..", "www", "assets", "cars")
MAX_W = 1000
QUALITY = 80

with open(os.path.join(BASE, "new_cars_downloaded_2_final.json"), encoding="utf-8") as f:
    cars = json.load(f)

total_in = 0
total_out = 0
for c in cars:
    src = os.path.join(RAW, c["slug"] + ".orig")
    dst = os.path.join(OUT, c["slug"] + ".jpg")
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    if w > MAX_W:
        new_h = round(h * MAX_W / w)
        im = im.resize((MAX_W, new_h), Image.LANCZOS)
    im.save(dst, "JPEG", quality=QUALITY, optimize=True)
    sin = os.path.getsize(src)
    sout = os.path.getsize(dst)
    total_in += sin
    total_out += sout
    print(f"{c['slug']:35s} {sin/1024:8.0f} KB -> {sout/1024:6.0f} KB  ({im.size[0]}x{im.size[1]})")

print(f"\nTotal: {total_in/1024/1024:.1f} MB -> {total_out/1024/1024:.1f} MB")
