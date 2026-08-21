import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE, "..", "www", "index.html")

with open(os.path.join(BASE, "full_zoom_export.txt"), encoding="utf-8") as f:
    EXPORT_TEXT = f.read()

pattern = re.compile(r'url:\s*"([^"]+)".*?anchorX:\s*([\-0-9.]+),\s*anchorY:\s*([\-0-9.]+),\s*maxScale:\s*([\-0-9.]+)')
updates = {}
for m in pattern.finditer(EXPORT_TEXT):
    url, ax, ay, ms = m.group(1), m.group(2), m.group(3), m.group(4)
    updates[url] = (ax, ay, ms)

print(f"Parsed {len(updates)} entries from export")

with open(HTML_PATH, encoding="utf-8") as f:
    html = f.read()

count = 0
unchanged = 0
not_found = []
for url, (ax, ay, ms) in updates.items():
    esc_url = re.escape(url)
    entry_pattern = re.compile(
        r'(url: "' + esc_url + r'"[^}]*?)anchorX: ([\-0-9.]+), anchorY: ([\-0-9.]+), maxScale: ([\-0-9.]+)'
    )
    m = entry_pattern.search(html)
    if not m:
        not_found.append(url)
        continue
    if m.group(2) == ax and m.group(3) == ay and m.group(4) == ms:
        unchanged += 1
        continue
    html = entry_pattern.sub(
        lambda mm: mm.group(1) + f"anchorX: {ax}, anchorY: {ay}, maxScale: {ms}", html, count=1
    )
    count += 1

with open(HTML_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(f"Updated {count} entries, {unchanged} already matched, {len(not_found)} not found")
if not_found:
    print("NOT FOUND:", not_found)

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
