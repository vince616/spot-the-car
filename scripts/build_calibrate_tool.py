import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    existing = json.load(f)
with open(os.path.join(BASE, "new_cars_downloaded.json"), encoding="utf-8") as f:
    new_cars = json.load(f)

ALL_NAMES = [c["name"] for c in existing] + [c["name_guess"] for c in new_cars]

# Rough category buckets for sensible default-distractor suggestions.
CATEGORY_KEYWORDS = {
    "luxury_sport": ["aston martin", "bentley", "lamborghini", "rolls-royce", "ferrari", "porsche", "db7", "db12", "urus", "gallardo"],
    "suv_van": ["kangoo", "espace", "kuga", "tiguan", "rav4", "grandland", "sportage", "f-pace", "range rover", "qashqai", "sorento", "wrangler", "defender", "cherokee", "duster", "colorado", "3008", "5008", "austral", "symbioz", "ariya", "aircross"],
    "classic": ["mini", "morris", "audi 100", "renault 4", "beetle", "favorit", "245", "326", "560 sel", "w123", "silver cloud", "e21", "2000 (classique)"],
    "electric": ["leaf", "dolphin", "mokka-e", "e-tech", "model y", "ariya"],
    "hot_hatch_compact": ["twingo", "golf", "clio", "208", "c2", "c3", "polo", "ibiza", "punto", "panda", "yaris", "corolla", "civic", "megane", "formentor"],
}

def categorize(name):
    n = name.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in n:
                return cat
    return "other"

pool = []
for c in existing:
    pool.append({"name": c["name"], "cat": categorize(c["name"])})
for c in new_cars:
    pool.append({"name": c["name_guess"], "cat": categorize(c["name_guess"])})

def default_distractors(name, exclude):
    cat = categorize(name)
    same_cat = [p["name"] for p in pool if p["cat"] == cat and p["name"] != name and p["name"] not in exclude]
    others = [p["name"] for p in pool if p["name"] != name and p["name"] not in exclude and p["name"] not in same_cat]
    # deterministic pseudo-shuffle so re-running the script gives stable results
    same_cat.sort(key=lambda s: (hash((name, s)) % 10000))
    others.sort(key=lambda s: (hash((name, s)) % 10000))
    picks = (same_cat + others)[:3]
    while len(picks) < 3:
        picks.append("???")
    return picks

pending = []
for c in new_cars:
    d = default_distractors(c["name_guess"], exclude={c["name_guess"]})
    pending.append({
        "slug": c["slug"],
        "wikiFile": c["wikiFile"],
        "url": f"assets/cars/{c['slug']}.jpg",
        "name": c["name_guess"],
        "anchorX": 50,
        "anchorY": 50,
        "maxScale": 2.6,
        "distractors": d,
    })

PENDING_JSON = json.dumps(pending, ensure_ascii=False)
ALL_NAMES_JSON = json.dumps(sorted(set(ALL_NAMES)), ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Calibrage - Spot the Car</title>
<style>
  :root{ --bg:#14141a; --surface:#1f2027; --surface-2:#2a2b34; --line:#38393f; --amber:#ffb020; --text:#f2f0ea; --muted:#9a9aa4; }
  *{ box-sizing:border-box; }
  body{ margin:0; background:var(--bg); color:var(--text); font-family:'Segoe UI',Arial,sans-serif; padding:16px; }
  h1{ font-size:20px; margin:0 0 4px; }
  .sub{ color:var(--muted); font-size:13px; margin-bottom:16px; }
  .toolbar{ position:sticky; top:0; background:var(--bg); padding:10px 0; z-index:10; display:flex; gap:10px; align-items:center; border-bottom:1px solid var(--line); margin-bottom:16px; flex-wrap:wrap; }
  button{ background:var(--amber); color:#1a1200; border:none; border-radius:8px; padding:10px 16px; font-weight:700; cursor:pointer; font-size:14px; }
  button.secondary{ background:var(--surface-2); color:var(--text); }
  .progress{ color:var(--muted); font-size:13px; }
  .grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:16px; }
  .card{ background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:12px; }
  .card.done{ border-color:#3fae6a; }
  .viewport-frame{ background:linear-gradient(145deg,#35363f,#1c1d23); border:1px solid var(--line); border-radius:12px; padding:5px; display:flex; justify-content:center; }
  .viewport{ position:relative; width:100%; aspect-ratio:1/1; max-width:320px; border-radius:8px; overflow:hidden; background:#0c0c0f; cursor:crosshair; }
  .viewport img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; transition:transform .05s linear; }
  .crosshair{ position:absolute; width:16px; height:16px; margin:-8px; border:2px solid var(--amber); border-radius:50%; pointer-events:none; box-shadow:0 0 0 1px rgba(0,0,0,.6); }
  .row{ display:flex; gap:8px; margin-top:8px; align-items:center; }
  .row label{ font-size:11px; color:var(--muted); width:70px; flex-shrink:0; }
  input[type=range]{ flex:1; }
  input[type=text]{ flex:1; background:var(--surface-2); border:1px solid var(--line); color:var(--text); border-radius:6px; padding:6px 8px; font-size:13px; }
  .readout{ font-family:monospace; font-size:11px; color:var(--muted); width:80px; text-align:right; }
  .fname{ font-size:11px; color:var(--muted); margin-top:6px; word-break:break-all; }
  .zoomtoggle{ display:flex; gap:6px; margin-top:6px; }
  .zoomtoggle button{ flex:1; padding:6px; font-size:12px; }
  textarea{ width:100%; height:300px; background:var(--surface-2); color:var(--text); border:1px solid var(--line); border-radius:8px; padding:10px; font-family:monospace; font-size:12px; margin-top:10px; }
  #exportPanel{ display:none; }
</style>
</head>
<body>
<h1>Calibrage des nouvelles voitures</h1>
<div class="sub">Clique sur l'image pour placer le point de zoom, ajuste le niveau de zoom initial, corrige le nom si besoin et les 3 mauvaises reponses. Tout est sauvegarde automatiquement dans ce navigateur. Aperçu identique au rendu en jeu (image recadree en carre avant le zoom, exactement comme dans l'app).</div>
<div class="toolbar">
  <button onclick="exportAll()">Exporter tout</button>
  <button class="secondary" onclick="resetAll()">Reinitialiser</button>
  <span class="progress" id="progress"></span>
</div>
<div id="exportPanel">
  <textarea id="exportText" readonly onclick="this.select()"></textarea>
</div>
<div class="grid" id="grid"></div>

<datalist id="nameList">__NAME_OPTIONS__</datalist>

<script>
const PENDING = __PENDING_JSON__;
const ALL_NAMES = __ALL_NAMES_JSON__;
const STORAGE_KEY = "spotthecar_calibration_v1";

function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw) return JSON.parse(raw);
  }catch(e){}
  return null;
}
function saveState(){
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();
if(!state || state.length !== PENDING.length){
  state = PENDING.map(c => ({...c}));
  saveState();
}

function updateProgress(){
  document.getElementById("progress").textContent = state.length + " voitures a calibrer";
}

function render(){
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  state.forEach((car, idx) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="viewport-frame">
        <div class="viewport" id="vp-${idx}">
          <img id="img-${idx}" src="${car.url}">
          <div class="crosshair" id="cross-${idx}"></div>
        </div>
      </div>
      <div class="fname">${car.wikiFile}</div>
      <div class="row">
        <label>Nom</label>
        <input type="text" list="nameList" value="${car.name.replace(/"/g,'&quot;')}" oninput="state[${idx}].name=this.value; saveState();">
      </div>
      <div class="row">
        <label>Zoom initial</label>
        <input type="range" min="1.2" max="6" step="0.1" value="${car.maxScale}" oninput="setScale(${idx}, this.value)">
        <span class="readout" id="scale-${idx}">x${Number(car.maxScale).toFixed(1)}</span>
      </div>
      <div class="row">
        <label>Ancrage</label>
        <span class="readout" id="anchor-${idx}">${Math.round(car.anchorX)}% / ${Math.round(car.anchorY)}%</span>
      </div>
      <div class="zoomtoggle">
        <button class="secondary" onclick="previewFull(${idx})">Voir sans zoom</button>
        <button class="secondary" onclick="previewZoom(${idx})">Voir zoom initial</button>
      </div>
      <div class="row"><label>Distracteur 1</label><input type="text" list="nameList" value="${car.distractors[0].replace(/"/g,'&quot;')}" oninput="state[${idx}].distractors[0]=this.value; saveState();"></div>
      <div class="row"><label>Distracteur 2</label><input type="text" list="nameList" value="${car.distractors[1].replace(/"/g,'&quot;')}" oninput="state[${idx}].distractors[1]=this.value; saveState();"></div>
      <div class="row"><label>Distracteur 3</label><input type="text" list="nameList" value="${car.distractors[2].replace(/"/g,'&quot;')}" oninput="state[${idx}].distractors[2]=this.value; saveState();"></div>
    `;
    grid.appendChild(card);

    const vp = card.querySelector(`#vp-${idx}`);
    vp.addEventListener("click", (e) => {
      const rect = vp.getBoundingClientRect();
      const x = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100));
      const y = Math.max(0, Math.min(100, ((e.clientY - rect.top) / rect.height) * 100));
      state[idx].anchorX = Math.round(x * 10) / 10;
      state[idx].anchorY = Math.round(y * 10) / 10;
      saveState();
      applyTransform(idx);
    });
    applyTransform(idx);
  });
  updateProgress();
}

function applyTransform(idx){
  const car = state[idx];
  const img = document.getElementById(`img-${idx}`);
  const cross = document.getElementById(`cross-${idx}`);
  img.style.transformOrigin = `${car.anchorX}% ${car.anchorY}%`;
  img.style.transform = `scale(${car.maxScale})`;
  cross.style.left = car.anchorX + "%";
  cross.style.top = car.anchorY + "%";
  document.getElementById(`anchor-${idx}`).textContent = `${Math.round(car.anchorX)}% / ${Math.round(car.anchorY)}%`;
}

function setScale(idx, val){
  state[idx].maxScale = parseFloat(val);
  document.getElementById(`scale-${idx}`).textContent = "x" + parseFloat(val).toFixed(1);
  saveState();
  applyTransform(idx);
}

function previewFull(idx){
  document.getElementById(`img-${idx}`).style.transform = "scale(1)";
}
function previewZoom(idx){
  applyTransform(idx);
}

function resetAll(){
  if(!confirm("Reinitialiser tous les reglages (zoom, ancrage, noms, distracteurs) ?")) return;
  state = PENDING.map(c => ({...c}));
  saveState();
  render();
}

function exportAll(){
  const lines = state.map(c => {
    const esc = s => String(s).replace(/\\\\/g,"\\\\\\\\").replace(/"/g,'\\\\"');
    const dis = c.distractors.map(d => `"${esc(d)}"`).join(", ");
    return `  { name: "${esc(c.name)}", url: "assets/cars/${c.slug}.jpg", wikiFile: "${c.wikiFile}", anchorX: ${c.anchorX}, anchorY: ${c.anchorY}, maxScale: ${c.maxScale}, distractors: [${dis}] },`;
  });
  const out = lines.join("\\n");
  document.getElementById("exportText").value = out;
  document.getElementById("exportPanel").style.display = "block";
  document.getElementById("exportPanel").scrollIntoView({behavior:"smooth"});
}

render();
</script>
</body>
</html>
"""

name_options = "".join(f'<option value="{n.replace(chr(34), "&quot;")}">' for n in sorted(set(ALL_NAMES)))
HTML = HTML.replace("__PENDING_JSON__", PENDING_JSON)
HTML = HTML.replace("__ALL_NAMES_JSON__", ALL_NAMES_JSON)
HTML = HTML.replace("__NAME_OPTIONS__", name_options)

out_path = os.path.join(BASE, "..", "www", "calibrate.html")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(HTML)
print("Wrote", out_path, "with", len(pending), "pending cars")
