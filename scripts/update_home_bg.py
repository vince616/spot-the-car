import base64, io
from PIL import Image

SRC = r"C:\Users\vincent.krief\Downloads\Spot the car page d'accueil v2.png"
HTML = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\www\index.html"

im = Image.open(SRC).convert("RGB")
TARGET_W = 853
if im.width > TARGET_W:
    new_h = round(im.height * TARGET_W / im.width)
    im = im.resize((TARGET_W, new_h), Image.LANCZOS)

buf = io.BytesIO()
im.save(buf, "JPEG", quality=85, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
print("new HOME_BG_B64 size:", len(buf.getvalue()), "bytes, image", im.size)

with open(HTML, encoding="utf-8") as f:
    lines = f.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith("const HOME_BG_B64"))
old_len = len(lines[idx])
lines[idx] = f'const HOME_BG_B64 = "{b64}";\n'
print(f"Replaced line {idx+1} (old length {old_len} -> new length {len(lines[idx])})")

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(lines)
