import json, os, subprocess, time

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw")

with open(os.path.join(BASE, "new_cars_downloaded.json"), encoding="utf-8") as f:
    cars = json.load(f)

def is_bad(path):
    if not os.path.exists(path) or os.path.getsize(path) < 20000:
        return True
    with open(path, "rb") as f:
        head = f.read(300)
    if b"Wikimedia Error" in head or b"<html" in head[:50].lower():
        return True
    return False

pending = [c for c in cars if is_bad(os.path.join(RAW, c["slug"] + ".orig"))]
print(f"{len(pending)} files still need downloading. Cooling down 90s first...", flush=True)
time.sleep(90)

failed = []
for i, c in enumerate(pending):
    out = os.path.join(RAW, c["slug"] + ".orig")
    attempt = 0
    ok = False
    while attempt < 4 and not ok:
        attempt += 1
        wait = 2 * attempt
        print(f"[{i+1}/{len(pending)}] {c['name_guess']} (try {attempt})...", flush=True)
        r = subprocess.run(
            ["curl", "-sS", "-L", "--ssl-no-revoke", "-A", "SpotTheCarBot/1.0 (contact: perso@example.local)",
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
    time.sleep(1.2)

print("\n=== DONE ===")
print("Still failed:", failed if failed else "none")
