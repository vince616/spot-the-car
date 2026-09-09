import json, os, subprocess, re, io, urllib.parse
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(BASE)

TARGETS = [
    {"slug": "audi-a4", "wikiFile": "Audi_A4_B9_sedans_(FL)_1X7A2441.jpg"},
    {"slug": "audi-tt", "wikiFile": "2019_Audi_TT_Sport_40_TFSi_S-A_2.0_Front.jpg"},
    {"slug": "mazda-mx-5", "wikiFile": "Mazda_Roadster_(MX-5)_by_Negawa_Bridge_(cropped).jpg"},
    {"slug": "renault-4", "wikiFile": "Renault_R4_BW_2016-07-17_13-45-32.jpg"},
    {"slug": "porsche-911-turbo-s", "wikiFile": "Porsche_992_Carrera_S_coupe_IMG_5832.jpg"},
]

UA = "SpotTheCarBot/1.0 (contact: perso@example.local)"

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
    print(f"OK {t['slug']}: {t['direct_url']}  | {t['artist']} | {t['license']}")

with open(os.path.join(BASE, "_replace5_meta.json"), "w", encoding="utf-8") as f:
    json.dump(TARGETS, f, ensure_ascii=False, indent=2)

print("\nDownloading + resizing...")
MAX_W = 1000
for t in TARGETS:
    if "direct_url" not in t:
        continue
    out_path = os.path.join(APP, "www", "assets", "cars", t["slug"] + ".jpg")
    r = subprocess.run(["curl.exe", "-sS", "-L", "--ssl-no-revoke", "-A", UA, "-o", out_path + ".tmp", t["direct_url"]],
                        capture_output=True, text=True)
    im = Image.open(out_path + ".tmp").convert("RGB")
    if im.width > MAX_W:
        new_h = round(im.height * MAX_W / im.width)
        im = im.resize((MAX_W, new_h), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=80, optimize=True)
    os.remove(out_path + ".tmp")
    print(f"Saved {out_path}  {im.size}")

print("Done.")
