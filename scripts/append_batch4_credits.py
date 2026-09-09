# -*- coding: utf-8 -*-
PATH = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\CREDITS_PHOTOS.txt"

ENTRIES = [
    ("Kia Picanto", "Kia%20Picanto,%20Auto%202024,%20Zurich%20(PANA0815).jpg",
     "Matti Blume", "CC BY-SA 4.0", "Own work"),
    ("Subaru Impreza (2002)", "2001-2002%20Subaru%20Impreza%20(GDE%20MY02)%20RS%20sedan%20(2011-06-15)%2001.jpg",
     "OSX", "Public domain", "Own work"),
    ("Renault Vel Satis", "Renault%20Vel%20Satis%203.0%20dCi%20V6%20%E2%80%93%20Frontansicht,%205.%20Mai%202012,%20Ratingen.jpg",
     "M 93", "CC BY-SA 3.0 de", "Own work"),
    ("Renault Avantime", "2002%20Renault%20Avantime%20Privilege%203.0%20Front.jpg",
     "Vauxford", "CC BY-SA 4.0", "Own work"),
    ("Maserati GranTurismo (2023)", "Maserati%20GranTurismo%20Trofeo%201X7A0828.jpg",
     "Alexander-93", "CC BY-SA 4.0", "Own work"),
    ("BMW X6 (E71)", "BMW%20X6%20xDrive30d%20(E71)%20%E2%80%93%20Frontansicht,%2026.%20M%C3%A4rz%202011,%20D%C3%BCsseldorf.jpg",
     "M 93", "Attribution", "Self-photographed"),
    ("Renault Clio II RS", "Clio%20RS%202.2.jpg",
     "RobindesB", "CC BY-SA 3.0", "Own work"),
    ("Renault Clio VI", "Renault%20Clio%20TCe%20115%20Techno%20(VI)%20%E2%80%93%20h%2017032026.jpg",
     "\u00a9 M 93", "CC BY-SA 3.0 de", "Own work"),
]

with open(PATH, encoding="utf-8") as f:
    text = f.read()

blocks = []
for name, wikifile, author, license_, source in ENTRIES:
    blocks.append(
        f"- {name}\n"
        f"  Fichier Wikimedia : {wikifile}\n"
        f"  Auteur            : {author}\n"
        f"  Licence           : {license_}\n"
        f"  Source            : {source}\n"
        f"  Page              : https://commons.wikimedia.org/wiki/File:{wikifile}\n"
    )

if not text.endswith("\n"):
    text += "\n"
text += "\n" + "\n".join(blocks)

with open(PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print(f"Appended {len(ENTRIES)} credit blocks")
