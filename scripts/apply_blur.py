import json, os
from PIL import Image, ImageFilter, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(BASE, "..", "www")
ZONES_PATH = os.path.join(BASE, "blur_zones.json")

with open(ZONES_PATH, encoding="utf-8") as f:
    zones = json.load(f)

BLUR_RADIUS = 50     # flou applique dans les zones (fort, pour rendre logos/textes illisibles)
FEATHER_RADIUS = 10  # flou du masque -> transition progressive sur les bords, pas de bord net
DILATE_PX = 10       # elargit chaque zone avant le degrade, pour que le coeur reste a 100%
                     # meme sur les petites zones (sinon le degrade "mange" toute la zone
                     # et le flou reste partiel -> logo encore visible en transparence)

# L'editeur affiche chaque photo dans un cadre fixe en 4:3 (aspect-ratio CSS du viewport)
# avec object-fit:contain. Comme la quasi-totalite des photos ne sont pas en 4:3 (surtout
# portrait), l'image reelle est affichee avec des marges vides (letterbox/pillarbox) a
# l'interieur de ce cadre. Les coordonnees exportees par l'outil sont relatives au CADRE,
# pas a l'image visible -- il faut donc les recaler sur l'image reelle avant de flouter.
CONTAINER_AR = 4 / 3

def correct_box(bx, by, bw, bh, img_w, img_h):
    img_ar = img_w / img_h
    if img_ar < CONTAINER_AR:
        # image plus "haute" que le cadre -> marges vides a gauche/droite
        rendered_frac = img_ar / CONTAINER_AR
        pad_frac = (1 - rendered_frac) / 2
        x = (bx / 100 - pad_frac) / rendered_frac * 100
        w = bw / rendered_frac
        y, h = by, bh
    elif img_ar > CONTAINER_AR:
        # image plus "large" que le cadre -> marges vides en haut/bas
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
    img_path = os.path.join(WWW, rel_path)
    if not os.path.exists(img_path):
        print("MANQUANT:", rel_path)
        continue
    im = Image.open(img_path).convert("RGB")
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
    result.save(img_path, "JPEG", quality=82, optimize=True)
    print(f"{rel_path}: {len(boxes)} zone(s) floutee(s)")

print(f"\nTermine : {len(zones)} photo(s), {total_boxes} zone(s) au total.")
