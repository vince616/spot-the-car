import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "icon-source.png")
OUT = os.path.join(BASE, "..", "www", "icons")
os.makedirs(OUT, exist_ok=True)

# RGB (pas de transparence) : iOS remplit les icones transparentes en noir.
# Le logo est centre dans l'image, donc la meme source sert aussi d'icone "maskable".
src = Image.open(SRC).convert("RGB")

SIZES = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "icon-maskable-512.png": 512,
    "apple-touch-icon.png": 180,
}
for name, size in SIZES.items():
    src.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
    print(f"Wrote www/icons/{name} ({size}x{size})")
