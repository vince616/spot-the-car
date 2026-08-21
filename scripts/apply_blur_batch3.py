import json, os
from PIL import Image, ImageFilter, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(BASE, "..", "www")
ZONES_PATH = os.path.join(BASE, "blur_zones_batch3.json")

with open(ZONES_PATH, encoding="utf-8") as f:
    zones = json.load(f)

BLUR_RADIUS = 50
FEATHER_RADIUS = 10
DILATE_PX = 10
CONTAINER_AR = 4 / 3

def correct_box(bx, by, bw, bh, img_w, img_h):
    img_ar = img_w / img_h
    if img_ar < CONTAINER_AR:
        rendered_frac = img_ar / CONTAINER_AR
        pad_frac = (1 - rendered_frac) / 2
        x = (bx / 100 - pad_frac) / rendered_frac * 100
        w = bw / rendered_frac
        y, h = by, bh
    elif img_ar > CONTAINER_AR:
        rendered_frac = CONTAINER_AR / img_ar
        pad_frac = (1 - rendered_frac) / 2
        y = (by / 100 - pad_frac) / rendered_frac * 100
        h = bh / rendered_frac
        x, w = bx, bw
    else:
        x, y, w, h = bx, by, bw, bh
    return x, y, w, h

total_boxes = 0
for rel_path, boxes in zones.items():
    src_path = os.path.join(WWW, rel_path)                              # original net (inchange)
    dst_path = os.path.join(WWW, rel_path.replace("assets/cars/", "assets/cars-blurred/"))
    if not os.path.exists(src_path):
        print("MANQUANT:", rel_path)
        continue
    im = Image.open(src_path).convert("RGB")
    w, h = im.size

    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    for (bx, by, bw, bh) in boxes:
        cx, cy, cw, ch = correct_box(bx, by, bw, bh, w, h)
        x0 = max(0, round(cx / 100 * w))
        y0 = max(0, round(cy / 100 * h))
        x1 = min(w, round((cx + cw) / 100 * w))
        y1 = min(h, round((cy + ch) / 100 * h))
        if x1 <= x0 or y1 <= y0:
            continue
        draw.rectangle([
            max(0, x0 - DILATE_PX), max(0, y0 - DILATE_PX),
            min(w, x1 + DILATE_PX), min(h, y1 + DILATE_PX),
        ], fill=255)
        total_boxes += 1

    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER_RADIUS))
    blurred = im.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    result = Image.composite(blurred, im, mask)
    result.save(dst_path, "JPEG", quality=82, optimize=True)
    print(f"{rel_path}: {len(boxes)} zone(s) floutee(s) -> {dst_path}")

print(f"\nTermine : {len(zones)} photo(s), {total_boxes} zone(s) au total.")
print("(originaux nets dans assets/cars/ non modifies)")
