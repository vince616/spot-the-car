import base64, io
from PIL import Image

SRC = r"C:\Users\vincent.krief\Downloads\ChatGPT Image 18 août 2026, 10_02_08.png"
HTML = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\www\index.html"

im = Image.open(SRC).convert("RGB")
TARGET_W = 700  # game screens don't need full-bleed sharpness, keep this one lean
if im.width > TARGET_W:
    new_h = round(im.height * TARGET_W / im.width)
    im = im.resize((TARGET_W, new_h), Image.LANCZOS)

buf = io.BytesIO()
im.save(buf, "JPEG", quality=78, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
print("GAME_BG_B64 size:", len(buf.getvalue()), "bytes, image", im.size)

with open(HTML, encoding="utf-8") as f:
    lines = f.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith("const SETTINGS_BG_B64"))
lines.insert(idx + 1, f'const GAME_BG_B64 = "{b64}";\n')

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(lines)

print(f"Inserted after line {idx+1}")
