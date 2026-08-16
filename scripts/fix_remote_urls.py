import re, os, unicodedata, json

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "..", "www", "index.html")
ASSETS = os.path.join(BASE, "..", "www", "assets", "cars")

def slugify(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower()
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n

with open(HTML, encoding="utf-8") as f:
    html = f.read()

start = html.index("const CARS = [")
end = html.index("\n];", start) + 3
block = html[start:end]

pattern = re.compile(r'(\{\s*name:\s*"((?:[^"\\]|\\.)*)",\s*url:\s*")((?:[^"\\]|\\.)*)("[^}]*\})')

fixed = []
missing = []

def repl(m):
    prefix, name, url, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
    if not url.startswith("http"):
        return m.group(0)
    slug = slugify(name)
    path = os.path.join(ASSETS, slug + ".jpg")
    if not os.path.exists(path):
        missing.append(name)
        return m.group(0)
    fixed.append(name)
    return prefix + f"assets/cars/{slug}.jpg" + suffix

new_block = pattern.sub(repl, block)
html = html[:start] + new_block + html[end:]

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(f"Fixed {len(fixed)} entries")
if missing:
    print(f"MISSING local file for {len(missing)} entries:")
    for n in missing:
        print(" -", n)

# keep cars.json in sync too
cars_json_path = os.path.join(BASE, "cars.json")
with open(cars_json_path, encoding="utf-8") as f:
    cars = json.load(f)
json_fixed = 0
for c in cars:
    if c["url"].startswith("http"):
        slug = slugify(c["name"])
        path = os.path.join(ASSETS, slug + ".jpg")
        if os.path.exists(path):
            c["url"] = f"assets/cars/{slug}.jpg"
            c["slug"] = slug
            json_fixed += 1
with open(cars_json_path, "w", encoding="utf-8") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)
print(f"cars.json: fixed {json_fixed} entries")
