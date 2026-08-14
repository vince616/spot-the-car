import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    cars = json.load(f)

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def fmt_num(n):
    return str(int(n)) if n == int(n) else str(n)

lines = ["const CARS = ["]
for i, c in enumerate(cars):
    dis = ", ".join(f'"{esc(d)}"' for d in c["distractors"])
    comma = "," if i < len(cars) - 1 else ""
    lines.append(
        f'  {{ name: "{esc(c["name"])}", url: "assets/cars/{c["slug"]}.jpg", '
        f'wikiFile: "{c["wikiFile"]}", '
        f'anchorX: {fmt_num(c["anchorX"])}, anchorY: {fmt_num(c["anchorY"])}, '
        f'maxScale: {fmt_num(c["maxScale"])}, distractors: [{dis}] }}{comma}'
    )
lines.append("];")

out = "\n".join(lines) + "\n"
with open(os.path.join(BASE, "cars_block_new.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("Wrote cars_block_new.txt,", len(cars), "entries")
