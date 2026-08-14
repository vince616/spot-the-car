import json, shlex

with open("cars.json", encoding="utf-8") as f:
    cars = json.load(f)

lines = ["#!/bin/bash", "set -e", "cd \"$(dirname \"$0\")/../raw\"", ""]
for c in cars:
    url = c["url"]
    out = c["slug"] + ".orig"
    lines.append(
        f'if [ ! -s {shlex.quote(out)} ]; then '
        f'echo "Downloading {c["name"]}..."; '
        f'curl -sS -L --ssl-no-revoke -A "Mozilla/5.0" -o {shlex.quote(out)} {shlex.quote(url)} || echo "FAILED: {c["name"]}"; '
        f'fi'
    )

with open("download_all.sh", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote download_all.sh with", len(cars), "entries")
