import json, os, re, unicodedata, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")
with open(os.path.join(BASE, "new_cars_downloaded_3.json"), encoding="utf-8") as f:
    cars = json.load(f)

by_slug = {c["slug"]: c for c in cars}

# Renames after visual inspection
RENAMES = {
    "a-identifier-paris-motor-show": "Seat Ateca",
}
for slug, new_name in RENAMES.items():
    if slug in by_slug:
        by_slug[slug]["name_guess"] = new_name

# True duplicates (litteralement la meme voiture, meme plaque, juste vue avant/arriere) --
# on garde la vue qui montre le plus d'elements identifiants (face avant).
DROP_SLUGS = {"volkswagen-t-cross-2"}

final = [c for c in cars if c["slug"] not in DROP_SLUGS]
print(f"{len(final)} cars kept (dropped {len(cars) - len(final)} duplicates)")

def slugify(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower()
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n

for c in final:
    new_slug = slugify(c["name_guess"])
    if new_slug != c["slug"]:
        old_orig = os.path.join(RAW, c["slug"] + ".orig")
        new_orig = os.path.join(RAW, new_slug + ".orig")
        if os.path.exists(old_orig) and not os.path.exists(new_orig):
            shutil.move(old_orig, new_orig)
            print(f"renamed raw file: {c['slug']}.orig -> {new_slug}.orig")
        c["slug"] = new_slug

with open(os.path.join(BASE, "new_cars_downloaded_3_final.json"), "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

for c in final:
    print(" -", c["name_guess"], "|", c["slug"])
