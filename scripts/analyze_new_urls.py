import re, urllib.parse, json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "new_urls.txt"), encoding="utf-8") as f:
    urls = [l.strip() for l in f if l.strip()]

def extract_filename(url):
    if "/wiki/File:" in url:
        return urllib.parse.unquote(url.split("/wiki/File:", 1)[1])
    if "upload.wikimedia.org" in url and "/thumb/" in url:
        # .../thumb/5/57/NAME.jpg/960px-NAME.jpg?...
        m = re.search(r'/thumb/[0-9a-f]/[0-9a-f]{2}/([^/]+)/', url)
        if m:
            return urllib.parse.unquote(m.group(1))
    return None

seen = {}
order = []
for u in urls:
    fname = extract_filename(u)
    if fname is None:
        print("COULD NOT PARSE:", u)
        continue
    if fname not in seen:
        seen[fname] = 0
        order.append(fname)
    seen[fname] += 1

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
existing_names_lower = {c["name"].lower() for c in existing}

print(f"{len(order)} unique files ({sum(seen.values())} links, {sum(seen.values())-len(order)} exact duplicate links)\n")
for fname in order:
    dup = f"  [x{seen[fname]} links]" if seen[fname] > 1 else ""
    print(fname, dup)
