import json, os, subprocess, re, time, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    cars = json.load(f)

def strip_tags(html):
    if not html:
        return "?"
    text = re.sub(r'<[^>]+>', '', html)
    return text.strip() or "?"

def batched(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

results = {}
BATCH = 15
for batch in batched(cars, BATCH):
    titles = "|".join("File:" + c["wikiFile"] for c in batch)
    url = ("https://commons.wikimedia.org/w/api.php?action=query&titles=" +
           urllib.parse.quote(titles, safe="|:%") +
           "&prop=imageinfo&iiprop=extmetadata&format=json")
    for attempt in range(5):
        r = subprocess.run(["curl", "-sS", "-L", "--ssl-no-revoke",
                             "-A", "SpotTheCarBot/1.0 (contact: vincent.krief@octopia.com)", url],
                            capture_output=True, text=True)
        try:
            data = json.loads(r.stdout)
            pages = data["query"]["pages"]
            break
        except Exception:
            print("retry batch...", r.stdout[:200])
            time.sleep(3)
            pages = {}
    for pid, p in pages.items():
        title = p.get("title", "")
        fname = title[len("File:"):] if title.startswith("File:") else title
        fname = fname.replace(" ", "_")
        info = p.get("imageinfo")
        if info:
            meta = info[0].get("extmetadata", {})
            artist = strip_tags(meta.get("Artist", {}).get("value"))
            license_ = meta.get("LicenseShortName", {}).get("value", "?")
            credit = strip_tags(meta.get("Credit", {}).get("value"))
        else:
            artist, license_, credit = "?", "?", "?"
        results[fname] = {"artist": artist, "license": license_, "credit": credit}
    time.sleep(1)

lines = []
lines.append("Credits photos — Wikimedia Commons (Spot the Car)")
lines.append("=" * 60)
lines.append("")
missing = []
for c in cars:
    key = urllib.parse.unquote(c["wikiFile"]).replace(" ", "_")
    r = results.get(key)
    if r is None:
        missing.append(c["name"])
        r = {"artist": "?", "license": "?", "credit": "?"}
    lines.append(f"- {c['name']}")
    lines.append(f"  Fichier Wikimedia : {c['wikiFile']}")
    lines.append(f"  Auteur            : {r['artist']}")
    lines.append(f"  Licence           : {r['license']}")
    lines.append(f"  Source            : {r['credit']}")
    lines.append(f"  Page              : https://commons.wikimedia.org/wiki/File:{c['wikiFile']}")
    lines.append("")

out_path = os.path.join(BASE, "..", "CREDITS_PHOTOS.txt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {out_path}")
print("Missing metadata for:", missing if missing else "none")
