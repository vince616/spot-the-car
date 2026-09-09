# -*- coding: utf-8 -*-
import json, os, subprocess
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(BASE)
UA = "SpotTheCarBot/1.0 (contact: perso@example.local)"
MAX_W = 1000

with open(os.path.join(BASE, "batch4_meta.json"), encoding="utf-8") as f:
    targets = json.load(f)

for t in targets:
    if "direct_url" not in t:
        continue
    out_path = os.path.join(APP, "www", "assets", "cars", t["slug"] + ".jpg")
    tmp = out_path + ".tmp"
    subprocess.run(["curl.exe", "-sS", "-L", "--ssl-no-revoke", "-A", UA, "-o", tmp, t["direct_url"]],
                   capture_output=True, text=True)
    im = Image.open(tmp).convert("RGB")
    if im.width > MAX_W:
        new_h = round(im.height * MAX_W / im.width)
        im = im.resize((MAX_W, new_h), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=80, optimize=True)
    os.remove(tmp)
    print(f"Saved {out_path}  {im.size}")

print("Done.")
