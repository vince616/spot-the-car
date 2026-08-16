import re, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "..", "www", "index.html")

with open(os.path.join(BASE, "full_catalog_export.txt"), encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(
    r'\{\s*name:\s*"(?P<name>(?:[^"\\]|\\.)*)",\s*'
    r'url:\s*"(?P<url>(?:[^"\\]|\\.)*)",\s*'
    r'wikiFile:\s*"(?P<wiki>(?:[^"\\]|\\.)*)",\s*'
    r'anchorX:\s*(?P<ax>-?[\d.]+),\s*'
    r'anchorY:\s*(?P<ay>-?[\d.]+),\s*'
    r'maxScale:\s*(?P<ms>[\d.]+),\s*'
    r'distractors:\s*\[(?P<dis>[^\]]*)\]\s*\}'
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

# Requested deletions
DELETE_NAMES = {"Chevrolet Colorado", "Peugeot 308 III"}
before = len(entries)
entries = [e for e in entries if e["name"] not in DELETE_NAMES]
print(f"Removed {before - len(entries)} entries ({', '.join(DELETE_NAMES)})")

# --- validation ---
problems = []
seen_names = set()
for e in entries:
    if len(e["distractors"]) != 3:
        problems.append(f"{e['name']}: has {len(e['distractors'])} distractors, expected 3")
    if "???" in e["distractors"] or e["name"] == "???":
        problems.append(f"{e['name']}: leftover placeholder")
    if e["name"] in seen_names:
        problems.append(f"{e['name']}: DUPLICATE name")
    seen_names.add(e["name"])
    if not (0 <= e["anchorX"] <= 100) or not (0 <= e["anchorY"] <= 100):
        problems.append(f"{e['name']}: anchor out of range ({e['anchorX']}, {e['anchorY']})")
    if not (1.0 <= e["maxScale"] <= 10):
        problems.append(f"{e['name']}: maxScale suspicious ({e['maxScale']})")

if problems:
    print("\n=== PROBLEMS ===")
    for p in problems:
        print(" -", p)
    raise SystemExit("Fix problems before applying")
else:
    print("No problems found.")

# resolve slug for local urls (assets/cars/<slug>.jpg), keep remote url as-is otherwise
def slug_from_url(url):
    if url.startswith("assets/cars/"):
        return url.split("/")[-1].rsplit(".", 1)[0]
    return None

# --- update cars.json (source-of-truth tracking file) ---
cars_json_entries = []
for e in entries:
    slug = slug_from_url(e["url"])
    entry = dict(e)
    if slug:
        entry["slug"] = slug
    cars_json_entries.append(entry)

with open(os.path.join(BASE, "cars.json"), "w", encoding="utf-8") as f:
    json.dump(cars_json_entries, f, ensure_ascii=False, indent=2)
print(f"cars.json updated: {len(cars_json_entries)} entries")

# --- build JS lines ---
def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def fmt_num(n):
    return str(int(n)) if n == int(n) else str(n)

lines = ["const CARS = ["]
for i, e in enumerate(entries):
    dis = ", ".join(f'"{esc(d)}"' for d in e["distractors"])
    comma = "," if i < len(entries) - 1 else ""
    lines.append(
        f'  {{ name: "{esc(e["name"])}", url: "{e["url"]}", '
        f'wikiFile: "{e["wikiFile"]}", '
        f'anchorX: {fmt_num(e["anchorX"])}, anchorY: {fmt_num(e["anchorY"])}, '
        f'maxScale: {fmt_num(e["maxScale"])}, distractors: [{dis}] }}{comma}'
    )
lines.append("];")
new_block = "\n".join(lines) + "\n"

# --- replace CARS block in index.html ---
with open(HTML, encoding="utf-8") as f:
    html_lines = f.readlines()

start = next(i for i, l in enumerate(html_lines) if l.strip() == "const CARS = [")
end = next(i for i in range(start, len(html_lines)) if html_lines[i].strip() == "];")
html_lines[start:end + 1] = [l + "\n" for l in new_block.rstrip("\n").split("\n")]

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(html_lines)

print(f"index.html CARS block replaced (lines {start+1}..{end+1} originally) with {len(entries)} entries")
