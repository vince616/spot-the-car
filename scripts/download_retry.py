import json, subprocess, time, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    cars = json.load(f)

def is_bad(path):
    if not os.path.exists(path) or os.path.getsize(path) < 20000:
        return True
    with open(path, "rb") as f:
        head = f.read(300)
    if b"Wikimedia Error" in head or b"<html" in head[:50].lower():
        return True
    return False

failed = []
for i, c in enumerate(cars):
    out = os.path.join(RAW, c["slug"] + ".orig")
    if not is_bad(out):
        continue
    attempt = 0
    ok = False
    while attempt < 6 and not ok:
        attempt += 1
        wait = 1.5 * attempt
        print(f"[{i+1}/{len(cars)}] {c['name']} (try {attempt})...", flush=True)
        r = subprocess.run(
            ["curl", "-sS", "-L", "--ssl-no-revoke", "-A", "SpotTheCarBot/1.0 (contact: vincent.krief@octopia.com)",
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
        failed.append(c["name"])
    time.sleep(0.8)

print("\n=== DONE ===")
print("Failed:", failed if failed else "none")
