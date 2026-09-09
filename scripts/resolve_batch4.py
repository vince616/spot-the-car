# -*- coding: utf-8 -*-
import json, subprocess, re, urllib.parse

UA = "SpotTheCarBot/1.0 (contact: perso@example.local)"

TARGETS = [
    {"slug": "kia-picanto", "wikiFile": "Kia Picanto, Auto 2024, Zurich (PANA0815).jpg"},
    {"slug": "subaru-impreza-gde", "wikiFile": "2001-2002 Subaru Impreza (GDE MY02) RS sedan (2011-06-15) 01.jpg"},
    {"slug": "renault-vel-satis", "wikiFile": "Renault Vel Satis 3.0 dCi V6 – Frontansicht, 5. Mai 2012, Ratingen.jpg"},
    {"slug": "renault-avantime", "wikiFile": "2002 Renault Avantime Privilege 3.0 Front.jpg"},
    {"slug": "maserati-granturismo", "wikiFile": "Maserati GranTurismo Trofeo 1X7A0828.jpg"},
    {"slug": "bmw-x6-e71", "wikiFile": "BMW X6 xDrive30d (E71) – Frontansicht, 26. März 2011, Düsseldorf.jpg"},
    {"slug": "renault-clio-ii-rs", "wikiFile": "Clio RS 2.2.jpg"},
    {"slug": "renault-clio-ii-phase1", "wikiFile": "Clio fase 1.jpg"},
    {"slug": "renault-clio-vi", "wikiFile": "Renault Clio TCe 115 Techno (VI) – h 17032026.jpg"},
]

def strip_tags(html):
    if not html:
        return "?"
    return re.sub(r'<[^>]+>', '', html).strip() or "?"

def curl_json(url):
    r = subprocess.run(["curl.exe", "-sS", "-L", "--ssl-no-revoke", "-A", UA, url],
                        capture_output=True, text=True)
    return json.loads(r.stdout)

for t in TARGETS:
    title = "File:" + t["wikiFile"]
    api = ("https://commons.wikimedia.org/w/api.php?action=query&titles=" +
           urllib.parse.quote(title, safe=":") +
           "&prop=imageinfo&iiprop=url|extmetadata&format=json")
    data = curl_json(api)
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    if "missing" in page:
        print(f"MISSING on Commons: {t['slug']} -> {title}")
        t["error"] = "missing"
        continue
    info = page["imageinfo"][0]
    t["direct_url"] = info["url"]
    meta = info.get("extmetadata", {})
    t["artist"] = strip_tags(meta.get("Artist", {}).get("value"))
    t["license"] = meta.get("LicenseShortName", {}).get("value", "?")
    t["credit"] = strip_tags(meta.get("Credit", {}).get("value"))
    t["canonical_title"] = page["title"][len("File:"):]
    print(f"OK {t['slug']}: {t['direct_url']}\n    artist={t['artist']} | license={t['license']} | credit={t['credit']}")

with open("batch4_meta.json", "w", encoding="utf-8") as f:
    json.dump(TARGETS, f, ensure_ascii=False, indent=2)
print("\nSaved batch4_meta.json")
