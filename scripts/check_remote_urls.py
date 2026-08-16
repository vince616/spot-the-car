import re

with open("../www/index.html", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'const CARS = \[(.*?)\n\];', html, re.S)
block = m.group(1)
pattern = re.compile(r'name:\s*"((?:[^"\\]|\\.)*)",\s*url:\s*"((?:[^"\\]|\\.)*)"')
names_urls = pattern.findall(block)
remote = [n for n, u in names_urls if u.startswith("http")]
local = [n for n, u in names_urls if not u.startswith("http")]
print("total", len(names_urls))
print("remote (broken offline):", len(remote))
print("local (ok):", len(local))
for n in remote:
    print(" -", n)
