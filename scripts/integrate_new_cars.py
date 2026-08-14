import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "..", "www", "index.html")

with open(os.path.join(BASE, "new_cars_calibrated.json"), encoding="utf-8") as f:
    new_entries = json.load(f)

for e in new_entries:
    e["slug"] = e["url"].split("/")[-1].rsplit(".", 1)[0]

# --- update cars.json (source-of-truth tracking file) ---
with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
existing.extend(new_entries)
with open(os.path.join(BASE, "cars.json"), "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print(f"cars.json now has {len(existing)} entries")

# --- build the JS lines to insert ---
def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def fmt_num(n):
    return str(int(n)) if n == int(n) else str(n)

new_lines = []
for e in new_entries:
    dis = ", ".join(f'"{esc(d)}"' for d in e["distractors"])
    new_lines.append(
        f'  {{ name: "{esc(e["name"])}", url: "{e["url"]}", '
        f'wikiFile: "{e["wikiFile"]}", '
        f'anchorX: {fmt_num(e["anchorX"])}, anchorY: {fmt_num(e["anchorY"])}, '
        f'maxScale: {fmt_num(e["maxScale"])}, distractors: [{dis}] }},'
    )

# --- insert into index.html, just before the CARS array's closing "];" ---
with open(HTML, encoding="utf-8") as f:
    lines = f.readlines()

start = next(i for i, l in enumerate(lines) if l.strip() == "const CARS = [")
end = next(i for i in range(start, len(lines)) if lines[i].strip() == "];")

# ensure the line right before "];" ends with a comma
prev_idx = end - 1
if not lines[prev_idx].rstrip().endswith(","):
    lines[prev_idx] = lines[prev_idx].rstrip("\n") + ",\n"

insertion = [l + "\n" for l in new_lines]
lines[end:end] = insertion

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(lines)

print(f"Inserted {len(new_entries)} new CARS entries into index.html (before line {end+1})")
