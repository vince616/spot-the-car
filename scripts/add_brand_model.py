import re, os
from brand_model_map import BRAND_MODEL

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "..", "www", "index.html")

with open(HTML, encoding="utf-8") as f:
    html = f.read()

start = html.index("const CARS = [")
end = html.index("\n];", start) + 3
block = html[start:end]

pattern = re.compile(r'(\{\s*name:\s*"((?:[^"\\]|\\.)*)",\s*url:\s*"(?:[^"\\]|\\.)*",\s*wikiFile:\s*"(?:[^"\\]|\\.)*",\s*)(anchorX:)')

missing = []

def repl(m):
    prefix, name = m.group(1), m.group(2)
    if name not in BRAND_MODEL:
        missing.append(name)
        return m.group(0)
    brand, model = BRAND_MODEL[name]
    brand_esc = brand.replace('\\', '\\\\').replace('"', '\\"')
    model_esc = model.replace('\\', '\\\\').replace('"', '\\"')
    return f'{prefix}brand: "{brand_esc}", model: "{model_esc}", {m.group(3)}'

new_block = pattern.sub(repl, block)
count = len(pattern.findall(block))
html = html[:start] + new_block + html[end:]

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(f"Processed {count} entries, {len(missing)} missing from BRAND_MODEL")
for n in missing:
    print(" - MISSING:", n)
