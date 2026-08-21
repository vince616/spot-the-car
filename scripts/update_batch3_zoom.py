import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE, "..", "www", "index.html")

# Colle ici exactement le bloc exporte par l'editeur de zoom pour les 26 voitures du batch 3.
EXPORT_TEXT = r'''
{ name: "Alfa Romeo Tonale", url: "assets/cars/alfa-romeo-tonale.jpg", wikiFile: "Alfa_Romeo_Tonale_1X7A0319.jpg", anchorX: 98.8, anchorY: 52.2, maxScale: 2.6, distractors: ["Alfa Romeo Giulia", "Audi Q2", "Mini Countryman"] },
{ name: "Alfa Romeo Junior", url: "assets/cars/alfa-romeo-junior.jpg", wikiFile: "Alfa_Romeo_Junior_IMG_0462.jpg", anchorX: 96.4, anchorY: 52.2, maxScale: 2.6, distractors: ["Alfa Romeo Tonale", "Audi Q2", "Opel Mokka-e"] },
{ name: "Alfa Romeo Junior (2)", url: "assets/cars/alfa-romeo-junior-2.jpg", wikiFile: "Alfa_Romeo_Junior_Auto_Zuerich_2024_DSC_6376.jpg", anchorX: 90.7, anchorY: 53.8, maxScale: 2.6, distractors: ["Alfa Romeo Giulia Quadrifoglio", "Audi Q2", "Ford Puma"] },
{ name: "Audi Q2", url: "assets/cars/audi-q2.jpg", wikiFile: "Audi_Q2_FL_1X7A0303.jpg", anchorX: 25.8, anchorY: 55.3, maxScale: 2.6, distractors: ["Audi TT", "BMW X6 M", "Mini Countryman"] },
{ name: "Dacia Spring", url: "assets/cars/dacia-spring.jpg", wikiFile: "2023_Dacia_Spring_1X7A6282.jpg", anchorX: 6.3, anchorY: 60.7, maxScale: 2.6, distractors: ["Dacia Sandero", "Fiat 500e", "Hyundai Inster"] },
{ name: "Citroen e-C5 Aircross", url: "assets/cars/citroen-e-c5-aircross.jpg", wikiFile: "Citro%C3%ABn_%C3%AB-C5_Aircross_Auto_Zuerich_2025_DSC_3486.jpg", anchorX: 88.8, anchorY: 55.2, maxScale: 2.6, distractors: ["Citroën C5 Aircross", "Peugeot 3008 II", "Renault Austral"] },
{ name: "BMW i8", url: "assets/cars/bmw-i8.jpg", wikiFile: "2016_BMW_i8.jpg", anchorX: 91.9, anchorY: 0.9, maxScale: 1.4, distractors: ["BMW X6 M", "Porsche 911", "Lamborghini Gallardo"] },
{ name: "Ford Explorer EV", url: "assets/cars/ford-explorer-ev.jpg", wikiFile: "Ford_Explorer_EV_IMG_2120.jpg", anchorX: 21.4, anchorY: 51.5, maxScale: 2.6, distractors: ["Ford Kuga", "Renault Megane E-Tech", "Volkswagen ID.5 GTX"] },
{ name: "Ford Capri (2024)", url: "assets/cars/ford-capri-2024.jpg", wikiFile: "Ford_Capri_(2024)_Autofr%C3%BChling_Ulm_2025_DSC_8745.jpg", anchorX: 97.3, anchorY: 16.7, maxScale: 2, distractors: ["Ford Puma", "Volkswagen ID.5 GTX", "BMW i8"] },
{ name: "Hyundai Inster", url: "assets/cars/hyundai-inster.jpg", wikiFile: "Hyundai_Inster_DSC_7945.jpg", anchorX: 25.6, anchorY: 68.2, maxScale: 2.6, distractors: ["Dacia Spring", "Fiat 500e", "Renault Twingo III"] },
{ name: "Suzuki Jimny", url: "assets/cars/suzuki-jimny.jpg", wikiFile: "Suzuki_Jimny_on_the_parking_near_%C3%9Eorbj%C3%B6rn_Mountain,_Iceland,_20230430_1630_3697.jpg", anchorX: 22.4, anchorY: 46.4, maxScale: 2.6, distractors: ["Jeep Wrangler", "Land Rover Defender", "Toyota Land Cruiser"] },
{ name: "Hyundai Kona", url: "assets/cars/hyundai-kona.jpg", wikiFile: "Hyundai_Kona_(SX2)_1X7A1647.jpg", anchorX: 78.4, anchorY: 50.1, maxScale: 2.6, distractors: ["Hyundai Ioniq 6", "Opel Mokka-e", "Nissan Qashqai"] },
{ name: "Hyundai Ioniq 6", url: "assets/cars/hyundai-ioniq-6.jpg", wikiFile: "Hyundai_Ioniq_6_1X7A7083.jpg", anchorX: 99.4, anchorY: 63.3, maxScale: 1.2, distractors: ["Tesla Model Y", "Volkswagen ID.5 GTX", "BMW i8"] },
{ name: "Jeep Renegade", url: "assets/cars/jeep-renegade.jpg", wikiFile: "2019_Jeep_Renegade_1.6_Multijet.jpg", anchorX: 70.9, anchorY: 45.3, maxScale: 2.6, distractors: ["Jeep Avenger", "Fiat 500X (2024)", "Opel Mokka-e"] },
{ name: "Jeep Avenger", url: "assets/cars/jeep-avenger.jpg", wikiFile: "Jeep_Avenger_IMG_7815.jpg", anchorX: 9.9, anchorY: 63.8, maxScale: 2.6, distractors: ["Jeep Renegade", "Fiat 500X (2024)", "Alfa Romeo Junior"] },
{ name: "Range Rover Evoque", url: "assets/cars/range-rover-evoque.jpg", wikiFile: "Range_Rover_Evoque_(L551)_1X7A7459.jpg", anchorX: 30.3, anchorY: 52.4, maxScale: 2.6, distractors: ["Range Rover", "Range Rover Sport SVR", "Land Rover Defender"] },
{ name: "Mini Countryman", url: "assets/cars/mini-countryman.jpg", wikiFile: "Mini_Countryman_(U25)_IMG_9521.jpg", anchorX: 0.7, anchorY: 55.3, maxScale: 2.6, distractors: ["Mini John Cooper Works", "Mini Cooper (1ere generation)", "Audi Q2"] },
{ name: "Peugeot 308", url: "assets/cars/peugeot-308.jpg", wikiFile: "Peugeot_308_C_1X7A7329.jpg", anchorX: 9.8, anchorY: 49.6, maxScale: 2.6, distractors: ["Peugeot 208 (Mk2)", "Peugeot 2008 II", "Renault Mégane"] },
{ name: "Skoda Fabia", url: "assets/cars/skoda-fabia.jpg", wikiFile: "Skoda_Fabia_IV_1X7A0388.jpg", anchorX: 1.2, anchorY: 67.8, maxScale: 2.6, distractors: ["Skoda Octavia", "Skoda Favorit", "Volkswagen Polo"] },
{ name: "Seat Ateca", url: "assets/cars/seat-ateca.jpg", wikiFile: "Paris_Motor_Show_2018,_Paris_(1Y7A2062).jpg", anchorX: 74.6, anchorY: 49, maxScale: 2.6, distractors: ["Seat Arona", "Volkswagen T-Roc (2021)", "Nissan Qashqai"] },
{ name: "Seat Arona", url: "assets/cars/seat-arona.jpg", wikiFile: "2019_SEAT_Arona_XCELLENCE_Lux_1.6.jpg", anchorX: 1.3, anchorY: 66, maxScale: 2.6, distractors: ["Seat Ateca", "Volkswagen T-Cross", "Opel Corsa"] },
{ name: "Toyota GR86", url: "assets/cars/toyota-gr86.jpg", wikiFile: "Toyota_GR86_SZ.jpg", anchorX: 1.1, anchorY: 63.8, maxScale: 2.6, distractors: ["Mazda MX-5", "Porsche 911", "BMW 323i (E21)"] },
{ name: "Volkswagen T-Cross", url: "assets/cars/volkswagen-t-cross.jpg", wikiFile: "Volkswagen_T-Cross_1X7A0366.jpg", anchorX: 2.7, anchorY: 71.1, maxScale: 2.6, distractors: ["Volkswagen T-Roc (2021)", "Seat Arona", "Peugeot 2008 II"] },
{ name: "Volkswagen T-Roc (2021)", url: "assets/cars/volkswagen-t-roc-2021.jpg", wikiFile: "Volkswagen_T-Roc_(2021)_1X7A0330.jpg", anchorX: 50, anchorY: 50, maxScale: 2.6, distractors: ["Volkswagen T-Cross", "Seat Ateca", "Audi Q2"] },
{ name: "Volkswagen ID.5 GTX", url: "assets/cars/volkswagen-id-5-gtx.jpg", wikiFile: "Volkswagen_ID.5_GTX_1X7A0318.jpg", anchorX: 50, anchorY: 50, maxScale: 2.6, distractors: ["Tesla Model Y", "Hyundai Ioniq 6", "Renault Megane E-Tech"] },
{ name: "Smart #3", url: "assets/cars/smart-3.jpg", wikiFile: "Smart_Hashtag_3_DSC_7992.jpg", anchorX: 91.6, anchorY: 48.6, maxScale: 2.6, distractors: ["Mini Countryman", "Fiat 500e", "Hyundai Kona"] },
'''

pattern = re.compile(r'url:\s*"([^"]+)".*?anchorX:\s*([\-0-9.]+),\s*anchorY:\s*([\-0-9.]+),\s*maxScale:\s*([\-0-9.]+)')
updates = {}
for m in pattern.finditer(EXPORT_TEXT):
    url, ax, ay, ms = m.group(1), m.group(2), m.group(3), m.group(4)
    updates[url] = (ax, ay, ms)

print(f"Parsed {len(updates)} entries from export")

with open(HTML_PATH, encoding="utf-8") as f:
    html = f.read()

count = 0
for url, (ax, ay, ms) in updates.items():
    esc_url = re.escape(url)
    entry_pattern = re.compile(
        r'(url: "' + esc_url + r'"[^}]*?)anchorX: [\-0-9.]+, anchorY: [\-0-9.]+, maxScale: [\-0-9.]+'
    )
    new_html, n = entry_pattern.subn(
        lambda m: m.group(1) + f"anchorX: {ax}, anchorY: {ay}, maxScale: {ms}", html
    )
    if n == 0:
        print("NON TROUVE:", url)
    else:
        count += n
        html = new_html

with open(HTML_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(f"Updated {count} entries in index.html")

# Meme mise a jour dans cars.json
CARS_JSON_PATH = os.path.join(BASE, "cars.json")
with open(CARS_JSON_PATH, encoding="utf-8") as f:
    cars = json.load(f)
updated_json = 0
for c in cars:
    if c["url"] in updates:
        ax, ay, ms = updates[c["url"]]
        c["anchorX"] = float(ax)
        c["anchorY"] = float(ay)
        c["maxScale"] = float(ms)
        updated_json += 1
with open(CARS_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)
print(f"Updated {updated_json} entries in cars.json")
