import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "new_cars_downloaded_3_final.json"), encoding="utf-8") as f:
    cars = json.load(f)

by_slug = {c["slug"]: c for c in cars}

BRAND_MODEL = {
    "alfa-romeo-tonale": ("Alfa Romeo", "Tonale"),
    "alfa-romeo-junior": ("Alfa Romeo", "Junior"),
    "alfa-romeo-junior-2": ("Alfa Romeo", "Junior"),
    "audi-q2": ("Audi", "Q2"),
    "dacia-spring": ("Dacia", "Spring"),
    "citroen-e-c5-aircross": ("Citroen", "e-C5 Aircross"),
    "bmw-i8": ("BMW", "i8"),
    "ford-explorer-ev": ("Ford", "Explorer"),
    "ford-capri-2024": ("Ford", "Capri"),
    "hyundai-inster": ("Hyundai", "Inster"),
    "suzuki-jimny": ("Suzuki", "Jimny"),
    "hyundai-kona": ("Hyundai", "Kona"),
    "hyundai-ioniq-6": ("Hyundai", "Ioniq 6"),
    "jeep-renegade": ("Jeep", "Renegade"),
    "jeep-avenger": ("Jeep", "Avenger"),
    "range-rover-evoque": ("Land Rover", "Range Rover Evoque"),
    "mini-countryman": ("Mini", "Countryman"),
    "peugeot-308": ("Peugeot", "308"),
    "skoda-fabia": ("Skoda", "Fabia"),
    "seat-ateca": ("Seat", "Ateca"),
    "seat-arona": ("Seat", "Arona"),
    "toyota-gr86": ("Toyota", "GR86"),
    "volkswagen-t-cross": ("Volkswagen", "T-Cross"),
    "volkswagen-t-roc-2021": ("Volkswagen", "T-Roc"),
    "volkswagen-id-5-gtx": ("Volkswagen", "ID.5"),
    "smart-3": ("Smart", "#3"),
}

DISTRACTORS = {
    "alfa-romeo-tonale": ["Alfa Romeo Giulia", "Audi Q2", "Mini Countryman"],
    "alfa-romeo-junior": ["Alfa Romeo Tonale", "Audi Q2", "Opel Mokka-e"],
    "alfa-romeo-junior-2": ["Alfa Romeo Giulia Quadrifoglio", "Audi Q2", "Ford Puma"],
    "audi-q2": ["Audi TT", "BMW X6 M", "Mini Countryman"],
    "dacia-spring": ["Dacia Sandero", "Fiat 500e", "Hyundai Inster"],
    "citroen-e-c5-aircross": ["Citroën C5 Aircross", "Peugeot 3008 II", "Renault Austral"],
    "bmw-i8": ["BMW X6 M", "Porsche 911", "Lamborghini Gallardo"],
    "ford-explorer-ev": ["Ford Kuga", "Renault Megane E-Tech", "Volkswagen ID.5 GTX"],
    "ford-capri-2024": ["Ford Puma", "Volkswagen ID.5 GTX", "BMW i8"],
    "hyundai-inster": ["Dacia Spring", "Fiat 500e", "Renault Twingo III"],
    "suzuki-jimny": ["Jeep Wrangler", "Land Rover Defender", "Toyota Land Cruiser"],
    "hyundai-kona": ["Hyundai Ioniq 6", "Opel Mokka-e", "Nissan Qashqai"],
    "hyundai-ioniq-6": ["Tesla Model Y", "Volkswagen ID.5 GTX", "BMW i8"],
    "jeep-renegade": ["Jeep Avenger", "Fiat 500X (2024)", "Opel Mokka-e"],
    "jeep-avenger": ["Jeep Renegade", "Fiat 500X (2024)", "Alfa Romeo Junior"],
    "range-rover-evoque": ["Range Rover", "Range Rover Sport SVR", "Land Rover Defender"],
    "mini-countryman": ["Mini John Cooper Works", "Mini Cooper (1ere generation)", "Audi Q2"],
    "peugeot-308": ["Peugeot 208 (Mk2)", "Peugeot 2008 II", "Renault Mégane"],
    "skoda-fabia": ["Skoda Octavia", "Skoda Favorit", "Volkswagen Polo"],
    "seat-ateca": ["Seat Arona", "Volkswagen T-Roc (2021)", "Nissan Qashqai"],
    "seat-arona": ["Seat Ateca", "Volkswagen T-Cross", "Opel Corsa"],
    "toyota-gr86": ["Mazda MX-5", "Porsche 911", "BMW 323i (E21)"],
    "volkswagen-t-cross": ["Volkswagen T-Roc (2021)", "Seat Arona", "Peugeot 2008 II"],
    "volkswagen-t-roc-2021": ["Volkswagen T-Cross", "Seat Ateca", "Audi Q2"],
    "volkswagen-id-5-gtx": ["Tesla Model Y", "Hyundai Ioniq 6", "Renault Megane E-Tech"],
    "smart-3": ["Mini Countryman", "Fiat 500e", "Hyundai Kona"],
}

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

entries = []
for c in cars:
    slug = c["slug"]
    brand, model = BRAND_MODEL[slug]
    dis = DISTRACTORS[slug]
    dis_str = ", ".join(f'"{esc(d)}"' for d in dis)
    line = (f'  {{ name: "{esc(c["name_guess"])}", url: "assets/cars/{slug}.jpg", '
            f'wikiFile: "{esc(c["wikiFile"])}", brand: "{esc(brand)}", model: "{esc(model)}", '
            f'anchorX: 50, anchorY: 50, maxScale: 2.6, distractors: [{dis_str}] }},')
    entries.append(line)

js_block = "\n".join(entries)
with open(os.path.join(BASE, "batch3_js_entries.txt"), "w", encoding="utf-8") as f:
    f.write(js_block)

# Also build the cars.json entries (same shape as existing entries there, no brand/model
# since cars.json doesn't carry those fields for any existing entry either)
json_entries = []
for c in cars:
    slug = c["slug"]
    dis = DISTRACTORS[slug]
    json_entries.append({
        "name": c["name_guess"],
        "url": f"assets/cars/{slug}.jpg",
        "wikiFile": c["wikiFile"],
        "anchorX": 50,
        "anchorY": 50,
        "maxScale": 2.6,
        "distractors": dis,
        "slug": slug,
    })

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
existing.extend(json_entries)
with open(os.path.join(BASE, "cars.json"), "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"Wrote batch3_js_entries.txt ({len(entries)} entries)")
print(f"Appended {len(json_entries)} entries to cars.json (now {len(existing)} total)")
