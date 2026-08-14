import re, json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "calibrated_export.txt"), encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(
    r'name:\s*"(?P<name>(?:[^"\\]|\\.)*)",\s*'
    r'url:\s*"(?P<url>(?:[^"\\]|\\.)*)",\s*'
    r'wikiFile:\s*"(?P<wiki>(?:[^"\\]|\\.)*)",\s*'
    r'anchorX:\s*(?P<ax>-?[\d.]+),\s*'
    r'anchorY:\s*(?P<ay>-?[\d.]+),\s*'
    r'maxScale:\s*(?P<ms>[\d.]+),\s*'
    r'distractors:\s*\[(?P<dis>[^\]]*)\]'
)

entries = []
for m in pattern.finditer(text):
    dis = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group('dis'))
    entries.append({
        "name": m.group('name'),
        "url": m.group('url'),
        "wikiFile": m.group('wiki'),
        "anchorX": float(m.group('ax')),
        "anchorY": float(m.group('ay')),
        "maxScale": float(m.group('ms')),
        "distractors": dis,
    })

print(f"Parsed {len(entries)} entries")

# --- validation ---
with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
existing_names = {c["name"] for c in existing}

problems = []
seen_names = set()
for e in entries:
    if len(e["distractors"]) != 3:
        problems.append(f"{e['name']}: has {len(e['distractors'])} distractors, expected 3")
    if "???" in e["distractors"] or e["name"] == "???":
        problems.append(f"{e['name']}: leftover placeholder '???'")
    if e["name"] in existing_names:
        problems.append(f"{e['name']}: DUPLICATE of an existing catalog name")
    if e["name"] in seen_names:
        problems.append(f"{e['name']}: DUPLICATE within the new batch itself")
    seen_names.add(e["name"])
    if not (0 <= e["anchorX"] <= 100) or not (0 <= e["anchorY"] <= 100):
        problems.append(f"{e['name']}: anchor out of 0-100 range ({e['anchorX']}, {e['anchorY']})")

if problems:
    print("\n=== PROBLEMS FOUND ===")
    for p in problems:
        print(" -", p)
else:
    print("No problems found.")

with open(os.path.join(BASE, "new_cars_calibrated.json"), "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
print("\nWrote new_cars_calibrated.json")
