import os
from PIL import Image

# Decor paysage de la version PC : visible sur les cotes de la "carte" de jeu (ecrans de question, score...).
SRC = r"C:\Users\vincent.krief\Downloads\Garage néon futuriste et Porsche argentée.png"
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "www", "assets", "pc", "bg-game.jpg")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

im = Image.open(SRC).convert("RGB")
print("source:", im.size)
im.save(OUT, "JPEG", quality=85, optimize=True, progressive=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
