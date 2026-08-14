import json, os, re, subprocess, time, unicodedata, urllib.parse
from new_cars_list import NEW_CARS

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")
OUT = os.path.join(BASE, "..", "www", "assets", "cars")

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
existing_slugs = {c["slug"] for c in existing}

def slugify(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower()
    n = re.sub(r'[^a-z0-9]+', '-', n).strip('-')
    return n

seen_slugs = set(existing_slugs)
for c in NEW_CARS:
    base_slug = slugify(c["name_guess"])
    slug = base_slug
    i = 2
    while slug in seen_slugs:
        slug = f"{base_slug}-{i}"
        i += 1
    seen_slugs.add(slug)
    c["slug"] = slug
    c["url"] = "https://commons.wikimedia.org/wiki/Special:FilePath/" + c["wikiFile"]

# --- download ---
def is_bad(path):
    if not os.path.exists(path) or os.path.getsize(path) < 20000:
        return True
    with open(path, "rb") as f:
        head = f.read(300)
    if b"Wikimedia Error" in head or b"<html" in head[:50].lower():
        return True
    return False

failed = []
for i, c in enumerate(NEW_CARS):
    out = os.path.join(RAW, c["slug"] + ".orig")
    if not is_bad(out):
        print(f"[{i+1}/{len(NEW_CARS)}] {c['name_guess']} - already downloaded, skip")
        continue
    attempt = 0
    ok = False
    while attempt < 6 and not ok:
        attempt += 1
        wait = 1.5 * attempt
        print(f"[{i+1}/{len(NEW_CARS)}] {c['name_guess']} (try {attempt})...", flush=True)
        r = subprocess.run(
            ["curl", "-sS", "-L", "--ssl-no-revoke", "-A", "SpotTheCarBot/1.0",
             "-o", out, "-w", "%{http_code}", c["url"]],
            capture_output=True, text=True
        )
        code = r.stdout.strip()
        if code == "200" and not is_bad(out):
            ok = True
            print(f"  OK ({os.path.getsize(out)} bytes)")
        else:
            print(f"  code={code} retrying in {wait}s...")
            time.sleep(wait)
    if not ok:
        failed.append(c["name_guess"])
    time.sleep(0.6)

print("\nDownload failures:", failed if failed else "none")

with open(os.path.join(BASE, "new_cars_downloaded.json"), "w", encoding="utf-8") as f:
    json.dump(NEW_CARS, f, ensure_ascii=False, indent=2)
print("Wrote new_cars_downloaded.json")
