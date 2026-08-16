import json, os, re, unicodedata, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")
with open(os.path.join(BASE, "new_cars_downloaded_2.json"), encoding="utf-8") as f:
    cars = json.load(f)

by_slug = {c["slug"]: c for c in cars}

# Rename ambiguous ones after visual inspection
RENAMES = {
    "citroen-a-identifier": "Citroen DS",
    "fiat-topolino": "Fiat Topolino (2023)",
    "fiat-500x": "Fiat 500X (2024)",
    "citroen-e-mehari": "Citroen e-Mehari (2016)",
    "citroen-traction-avant": "Citroen Traction Avant 11B",
    "ds-4-e-tense": "DS 4 E-Tense (2021)",
    "peugeot-3008": "Peugeot 3008 (2023)",
    "peugeot-5008": "Peugeot 5008 (2024)",
    "nissan-note": "Nissan Note (2009)",
    "mg-3-hybrid": "MG 3 Hybrid (2024)",
    "jaecoo-5": "Jaecoo 5 (2025)",
    "porsche-macan": "Porsche Macan Electrique (2024)",
    "nissan-patrol": "Nissan Patrol (2019)",
    "nissan-juke": "Nissan Juke (2019)",
    "tesla-cybertruck-2": "Tesla Cybertruck (2024)",
    "lexus-lbx-2": "Lexus LBX (2024)",
}
for slug, new_name in RENAMES.items():
    if slug in by_slug:
        by_slug[slug]["name_guess"] = new_name

# Drop true duplicates (same exact car/generation, different photo, no distinguishing
# value in keeping both) -- keep the better-angled photo of each pair.
DROP_SLUGS = {"tesla-cybertruck", "lexus-lbx"}

final = [c for c in cars if c["slug"] not in DROP_SLUGS]
print(f"{len(final)} cars kept (dropped {len(cars) - len(final)} duplicates)")

def slugify(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower()
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n

# regenerate the slug from the final name where it was renamed, and rename the
# already-downloaded .orig file on disk to match
for c in final:
    new_slug = slugify(c["name_guess"])
    if new_slug != c["slug"]:
        old_orig = os.path.join(RAW, c["slug"] + ".orig")
        new_orig = os.path.join(RAW, new_slug + ".orig")
        if os.path.exists(old_orig) and not os.path.exists(new_orig):
            shutil.move(old_orig, new_orig)
            print(f"renamed raw file: {c['slug']}.orig -> {new_slug}.orig")
        c["slug"] = new_slug

with open(os.path.join(BASE, "new_cars_downloaded_2_final.json"), "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

for c in final:
    print(" -", c["name_guess"], "|", c["slug"])
