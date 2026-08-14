import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\vincent.krief\Downloads\spot-the-car_21.html"
DST = os.path.join(BASE, "..", "index.html")

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

# --- 1. replace CARS block, found by content search (robust to line shifts) ---
start = next(i for i, l in enumerate(lines) if l.strip() == "const CARS = [")
end = next(i for i in range(start, len(lines)) if lines[i].strip() == "];")
with open(os.path.join(BASE, "cars_block_new.txt"), encoding="utf-8") as f:
    new_block = f.readlines()
lines[start:end + 1] = new_block
print(f"CARS block: replaced lines {start+1}..{end+1} ({end-start+1} lines) with {len(new_block)} lines")

# --- 2. simplify imgUrl() now that every CARS entry has a local url ---
fn_start = next(i for i, l in enumerate(lines) if l.strip() == "function imgUrl(car){")
fn_end = next(i for i in range(fn_start, len(lines)) if lines[i].strip() == "}")
old_fn = "".join(lines[fn_start:fn_end + 1])
assert "car.url" in old_fn and "car.file" in old_fn, old_fn
lines[fn_start:fn_end + 1] = [
    "function imgUrl(car){\n",
    "  return car.url;\n",
    "}\n",
]
print(f"imgUrl(): replaced lines {fn_start+1}..{fn_end+1}")

# --- 3. fix broken credit link (was car.file, which no CARS entry ever had) ---
credit_idx = next(i for i, l in enumerate(lines) if "COMMONS_FILE_PAGE + encodeURIComponent(car.file)" in l)
lines[credit_idx] = lines[credit_idx].replace(
    "COMMONS_FILE_PAGE + encodeURIComponent(car.file)",
    "COMMONS_FILE_PAGE + car.wikiFile"
)
print(f"credit link: fixed line {credit_idx+1}")

with open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(lines)

print("Wrote", DST, "-", len(lines), "lines")
