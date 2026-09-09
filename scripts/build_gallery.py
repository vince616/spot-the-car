import json

CARS_JSON = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\scripts\cars.json"
OUT = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\www\gallery.html"

with open(CARS_JSON, encoding="utf-8") as f:
    cars = json.load(f)

cars_sorted = sorted(cars, key=lambda c: c["name"].lower())

cards = []
for c in cars_sorted:
    cards.append(f'''
    <div class="card">
      <img src="{c['url']}" alt="{c['name']}" loading="lazy">
      <div class="cap">{c['name']}</div>
    </div>''')

html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Galerie complete - {len(cars)} voitures</title>
<style>
  body {{ margin:0; padding:20px; background:#0c0c0f; color:#fff; font-family: system-ui, sans-serif; }}
  h1 {{ font-size:18px; margin-bottom:16px; }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap:12px; }}
  .card {{ background:#1a1a20; border-radius:8px; overflow:hidden; border:1px solid #333; }}
  .card img {{ width:100%; height:120px; object-fit:cover; display:block; }}
  .cap {{ font-size:12px; padding:6px 8px; }}
</style>
</head>
<body>
  <h1>Catalogue complet -- {len(cars)} voitures (photos nettes, telles qu'affichees a la revelation)</h1>
  <div class="grid">{''.join(cards)}</div>
</body>
</html>
'''

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(f"Wrote {OUT} with {len(cars)} cars")
