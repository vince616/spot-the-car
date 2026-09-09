import json, re

with open('scripts/blur_zones.json', encoding='utf-8') as f:
    zones = json.load(f)
EXTRA_NO_ZONE_DATA = {
    "assets/cars/citroen-traction-avant-11b.jpg",
    "assets/cars/renault-espace-iii.jpg",
}
keys = sorted(set(zones.keys()) | EXTRA_NO_ZONE_DATA)

with open('www/index.html', encoding='utf-8') as f:
    html = f.read()

lines = [f'  "{k}",' for k in keys]
lines[-1] = lines[-1].rstrip(",")
new_block = "const BLURRED_CARS = new Set([\n" + "\n".join(lines) + "\n]);"

pattern = re.compile(r'const BLURRED_CARS = new Set\(\[.*?\]\);', re.S)
html2, n = pattern.subn(new_block, html, count=1)
assert n == 1, f"expected 1 replacement, got {n}"

with open('www/index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(html2)

print(f"BLURRED_CARS set rewritten with {len(keys)} entries")
