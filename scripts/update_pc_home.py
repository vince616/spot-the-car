import os
from PIL import Image

# Visuel d'accueil de la version PC (paysage) : accueil + choix du mode sur un seul ecran.
SRC = r"C:\Users\vincent.krief\Downloads\Menu néon du garage cyberpunk.png"
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "www", "assets", "pc", "home-pc.jpg")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

im = Image.open(SRC).convert("RGB")
print("source:", im.size)
im.save(OUT, "JPEG", quality=86, optimize=True, progressive=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
