import json, os
from PIL import Image, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(BASE, "..", "www")
ZONES_PATH = os.path.join(BASE, "blur_zones.json")

with open(ZONES_PATH, encoding="utf-8") as f:
    zones = json.load(f)

BLUR_RADIUS = 18

total_boxes = 0
for rel_path, boxes in zones.items():
    img_path = os.path.join(WWW, rel_path)
    if not os.path.exists(img_path):
        print("MANQUANT:", rel_path)
        continue
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    for (bx, by, bw, bh) in boxes:
        x0 = max(0, round(bx / 100 * w))
        y0 = max(0, round(by / 100 * h))
        x1 = min(w, round((bx + bw) / 100 * w))
        y1 = min(h, round((by + bh) / 100 * h))
        if x1 <= x0 or y1 <= y0:
            continue
        region = im.crop((x0, y0, x1, y1))
        region = region.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
        im.paste(region, (x0, y0))
        total_boxes += 1
    im.save(img_path, "JPEG", quality=82, optimize=True)
    print(f"{rel_path}: {len(boxes)} zone(s) floutee(s)")

print(f"\nTermine : {len(zones)} photo(s), {total_boxes} zone(s) au total.")
