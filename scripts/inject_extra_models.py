import json, os
from extra_models import EXTRA_MODELS_BY_BRAND

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "..", "www", "index.html")

with open(HTML, encoding="utf-8") as f:
    lines = f.readlines()

old_block = '''// Mode Expert : marque/modele deduits du catalogue, pour les listes deroulantes
const ALL_BRANDS = [...new Set(CARS.map(c => c.brand))].sort();
const MODELS_BY_BRAND = {};
CARS.forEach(c => {
  if(!MODELS_BY_BRAND[c.brand]) MODELS_BY_BRAND[c.brand] = new Set();
  MODELS_BY_BRAND[c.brand].add(c.model);
});
Object.keys(MODELS_BY_BRAND).forEach(b => { MODELS_BY_BRAND[b] = [...MODELS_BY_BRAND[b]].sort(); });
const ALL_MODELS = [...new Set(CARS.map(c => c.model))].sort();
'''

extras_json = json.dumps(EXTRA_MODELS_BY_BRAND, ensure_ascii=False)

new_block = f'''// Mode Expert : marque/modele deduits du catalogue, pour les listes deroulantes.
// EXTRA_MODELS_BY_BRAND ajoute de vrais modeles supplementaires (sans photo) pour
// garantir au moins ~6 choix par marque meme quand le catalogue photo n'en a qu'1 ou 2
// -- sinon la liste "Modele" trahirait presque la reponse a elle seule.
const EXTRA_MODELS_BY_BRAND = {extras_json};
const ALL_BRANDS = [...new Set(CARS.map(c => c.brand))].sort();
const MODELS_BY_BRAND = {{}};
CARS.forEach(c => {{
  if(!MODELS_BY_BRAND[c.brand]) MODELS_BY_BRAND[c.brand] = new Set();
  MODELS_BY_BRAND[c.brand].add(c.model);
}});
Object.keys(MODELS_BY_BRAND).forEach(b => {{
  (EXTRA_MODELS_BY_BRAND[b] || []).forEach(m => MODELS_BY_BRAND[b].add(m));
  MODELS_BY_BRAND[b] = [...MODELS_BY_BRAND[b]].sort();
}});
const ALL_MODELS = [...new Set(CARS.map(c => c.model))].sort();
'''

full_text = "".join(lines)
assert old_block in full_text, "old_block not found verbatim"
full_text = full_text.replace(old_block, new_block)

with open(HTML, "w", encoding="utf-8", newline="\n") as f:
    f.write(full_text)

print("Injected EXTRA_MODELS_BY_BRAND for", len(EXTRA_MODELS_BY_BRAND), "brands")
