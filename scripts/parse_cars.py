import re, json, unicodedata

with open("cars_raw.txt", encoding="utf-8") as f:
    lines = [l for l in f if l.strip().startswith("{")]

pattern = re.compile(
    r'name:\s*"(?P<name>(?:[^"\\]|\\.)*)",\s*'
    r'url:\s*"(?P<url>(?:[^"\\]|\\.)*)",\s*'
    r'anchorX:\s*(?P<ax>[\d.]+),\s*'
    r'anchorY:\s*(?P<ay>[\d.]+),\s*'
    r'maxScale:\s*(?P<ms>[\d.]+),\s*'
    r'distractors:\s*\[(?P<dis>[^\]]*)\]'
)

def slugify(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower()
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n

cars = []
seen_slugs = {}
for l in lines:
    m = pattern.search(l)
    if not m:
        print("NO MATCH:", l)
        continue
    dis_raw = m.group('dis')
    dis = re.findall(r'"((?:[^"\\]|\\.)*)"', dis_raw)
    slug = slugify(m.group('name'))
    if slug in seen_slugs:
        seen_slugs[slug] += 1
        slug = f"{slug}-{seen_slugs[slug]}"
    else:
        seen_slugs[slug] = 1
    wiki_file = m.group('url').split("Special:FilePath/", 1)[1]
    cars.append({
        "name": m.group('name'),
        "url": m.group('url'),
        "wikiFile": wiki_file,
        "slug": slug,
        "anchorX": float(m.group('ax')),
        "anchorY": float(m.group('ay')),
        "maxScale": float(m.group('ms')),
        "distractors": dis
    })

print(f"Parsed {len(cars)} cars")
with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)
