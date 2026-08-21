import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "cars.json"), encoding="utf-8") as f:
    CARS = json.load(f)

CARDS = [{"name": c["name"], "url": c["url"]} for c in CARS]
CARDS_JSON = json.dumps(CARDS, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Editeur de flou - Spot the Car</title>
<style>
  :root{ --bg:#14141a; --surface:#1f2027; --surface-2:#2a2b34; --line:#38393f; --amber:#ffb020; --text:#f2f0ea; --muted:#9a9aa4; --good:#3fae6a; }
  *{ box-sizing:border-box; }
  body{ margin:0; background:var(--bg); color:var(--text); font-family:'Segoe UI',Arial,sans-serif; padding:16px; }
  h1{ font-size:20px; margin:0 0 4px; }
  .sub{ color:var(--muted); font-size:13px; margin-bottom:16px; max-width:900px; }
  .toolbar{ position:sticky; top:0; background:var(--bg); padding:10px 0; z-index:10; display:flex; gap:10px; align-items:center; border-bottom:1px solid var(--line); margin-bottom:16px; flex-wrap:wrap; }
  button{ background:var(--amber); color:#1a1200; border:none; border-radius:8px; padding:10px 16px; font-weight:700; cursor:pointer; font-size:14px; }
  button.secondary{ background:var(--surface-2); color:var(--text); }
  button.small{ padding:4px 8px; font-size:12px; border-radius:6px; }
  .progress{ color:var(--muted); font-size:13px; }
  #search{ background:var(--surface-2); border:1px solid var(--line); color:var(--text); border-radius:8px; padding:9px 12px; font-size:14px; min-width:220px; }
  label.chk{ font-size:13px; color:var(--muted); display:flex; align-items:center; gap:6px; }
  .grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(360px,1fr)); gap:16px; }
  .card{ background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:12px; position:relative; }
  .card.done{ border-color:var(--good); }
  .card.hidden{ display:none; }
  .badge{ position:absolute; top:10px; right:10px; font-size:10px; font-weight:700; padding:3px 7px; border-radius:5px; background:var(--good); color:#041f0e; }
  .name{ font-size:14px; font-weight:700; margin-bottom:8px; }
  .viewport-frame{ background:linear-gradient(145deg,#35363f,#1c1d23); border:1px solid var(--line); border-radius:12px; padding:5px; }
  .viewport{ position:relative; width:100%; aspect-ratio:4/3; border-radius:8px; overflow:hidden; background:#0c0c0f; cursor:crosshair; user-select:none; }
  .viewport img{ position:absolute; inset:0; width:100%; height:100%; object-fit:contain; pointer-events:none; }
  .box{ position:absolute; border:2px solid var(--amber); background:rgba(255,176,32,0.25); box-sizing:border-box; }
  .box .del{ position:absolute; top:-10px; right:-10px; width:20px; height:20px; border-radius:50%; background:#c0392b; color:#fff; font-size:12px; line-height:20px; text-align:center; cursor:pointer; font-weight:700; }
  .draft{ position:absolute; border:2px dashed var(--amber); background:rgba(255,176,32,0.15); box-sizing:border-box; pointer-events:none; }
  .boxlist{ font-size:11px; color:var(--muted); margin-top:8px; }
  .fname{ font-size:11px; color:var(--muted); margin-top:6px; word-break:break-all; }
  textarea{ width:100%; height:400px; background:var(--surface-2); color:var(--text); border:1px solid var(--line); border-radius:8px; padding:10px; font-family:monospace; font-size:12px; margin-top:10px; }
  #exportPanel{ display:none; }
</style>
</head>
<body>
<h1>Editeur de flou - logos &amp; badges</h1>
<div class="sub">Pour chaque photo, clique-glisse un rectangle sur chaque logo/badge/nom de modele visible (calandre, jantes, feux, plaque...). Plusieurs rectangles possibles par photo. Clique sur le rond rouge pour supprimer un rectangle. Tout se sauvegarde automatiquement dans ce navigateur. Une fois termine, clique sur "Exporter" et colle le resultat a Claude.</div>
<div class="toolbar">
  <input type="text" id="search" placeholder="Rechercher une voiture par nom..." oninput="applyFilter()">
  <label class="chk"><input type="checkbox" id="onlyTodo" onchange="applyFilter()"> Sans rectangle uniquement</label>
  <button onclick="exportAll()">Exporter les zones a flouter</button>
  <button class="secondary" onclick="resetAll()">Tout reinitialiser</button>
  <span class="progress" id="progress"></span>
</div>
<div id="exportPanel">
  <div class="sub" id="exportLabel"></div>
  <textarea id="exportText" readonly onclick="this.select()"></textarea>
</div>
<div class="grid" id="grid"></div>

<script>
const CARDS = __CARDS_JSON__;
const STORAGE_KEY = "spotthecar_blureditor_v1";

function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw){
      const parsed = JSON.parse(raw);
      if(parsed.length === CARDS.length) return parsed;
    }
  }catch(e){}
  return CARDS.map(() => []);
}
function saveState(){
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState(); // state[idx] = [{x,y,w,h}, ...] en pourcentage de l'image affichee

function updateProgress(){
  const done = state.filter(b => b.length > 0).length;
  document.getElementById("progress").textContent = `${CARDS.length} voitures - ${done} avec au moins une zone floutee`;
}

function render(){
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  CARDS.forEach((car, idx) => {
    const card = document.createElement("div");
    card.className = "card" + (state[idx].length > 0 ? " done" : "");
    card.dataset.name = car.name.toLowerCase();
    card.dataset.todo = state[idx].length > 0 ? "0" : "1";
    card.innerHTML = `
      ${state[idx].length > 0 ? `<div class="badge">${state[idx].length} zone(s)</div>` : ''}
      <div class="name">${car.name}</div>
      <div class="viewport-frame">
        <div class="viewport" id="vp-${idx}">
          <img id="img-${idx}" src="${car.url}">
        </div>
      </div>
      <div class="fname">${car.url}</div>
      <div class="boxlist" id="list-${idx}"></div>
    `;
    grid.appendChild(card);
    setupViewport(idx);
    renderBoxes(idx);
  });
  updateProgress();
  applyFilter();
}

function renderBoxes(idx){
  const vp = document.getElementById(`vp-${idx}`);
  vp.querySelectorAll(".box").forEach(el => el.remove());
  state[idx].forEach((b, bi) => {
    const el = document.createElement("div");
    el.className = "box";
    el.style.left = b.x + "%";
    el.style.top = b.y + "%";
    el.style.width = b.w + "%";
    el.style.height = b.h + "%";
    el.innerHTML = `<div class="del" onclick="event.stopPropagation(); removeBox(${idx}, ${bi})">&times;</div>`;
    vp.appendChild(el);
  });
  document.getElementById(`list-${idx}`).textContent = state[idx].length
    ? state[idx].map((b,i) => `#${i+1}: ${b.x.toFixed(1)}%,${b.y.toFixed(1)}% ${b.w.toFixed(1)}x${b.h.toFixed(1)}%`).join(" | ")
    : "Aucune zone.";
}

function removeBox(idx, bi){
  state[idx].splice(bi, 1);
  saveState();
  renderBoxes(idx);
  refreshCardBadge(idx);
}

function refreshCardBadge(idx){
  const cards = document.getElementById("grid").children;
  const card = cards[idx];
  card.classList.toggle("done", state[idx].length > 0);
  card.dataset.todo = state[idx].length > 0 ? "0" : "1";
  let badge = card.querySelector(".badge");
  if(state[idx].length > 0){
    if(!badge){
      badge = document.createElement("div");
      badge.className = "badge";
      card.insertBefore(badge, card.firstChild);
    }
    badge.textContent = `${state[idx].length} zone(s)`;
  } else if(badge){
    badge.remove();
  }
  updateProgress();
}

function setupViewport(idx){
  const vp = document.getElementById(`vp-${idx}`);
  let drafting = false, startX = 0, startY = 0, draftEl = null;

  function pct(e){
    const rect = vp.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const x = Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width) * 100));
    const y = Math.max(0, Math.min(100, ((clientY - rect.top) / rect.height) * 100));
    return {x, y};
  }

  function down(e){
    if(e.target.classList.contains("del")) return;
    e.preventDefault();
    drafting = true;
    const p = pct(e);
    startX = p.x; startY = p.y;
    draftEl = document.createElement("div");
    draftEl.className = "draft";
    draftEl.style.left = startX + "%";
    draftEl.style.top = startY + "%";
    vp.appendChild(draftEl);
  }
  function move(e){
    if(!drafting) return;
    e.preventDefault();
    const p = pct(e);
    const x = Math.min(startX, p.x), y = Math.min(startY, p.y);
    const w = Math.abs(p.x - startX), h = Math.abs(p.y - startY);
    draftEl.style.left = x + "%"; draftEl.style.top = y + "%";
    draftEl.style.width = w + "%"; draftEl.style.height = h + "%";
  }
  function up(e){
    if(!drafting) return;
    drafting = false;
    const rect = draftEl.getBoundingClientRect();
    const vpRect = vp.getBoundingClientRect();
    const x = ((rect.left - vpRect.left) / vpRect.width) * 100;
    const y = ((rect.top - vpRect.top) / vpRect.height) * 100;
    const w = (rect.width / vpRect.width) * 100;
    const h = (rect.height / vpRect.height) * 100;
    draftEl.remove();
    draftEl = null;
    if(w > 1 && h > 1){
      state[idx].push({x, y, w, h});
      saveState();
      renderBoxes(idx);
      refreshCardBadge(idx);
    }
  }

  vp.addEventListener("mousedown", down);
  vp.addEventListener("mousemove", move);
  window.addEventListener("mouseup", up);
  vp.addEventListener("touchstart", down, {passive:false});
  vp.addEventListener("touchmove", move, {passive:false});
  vp.addEventListener("touchend", up);
}

function resetAll(){
  if(!confirm("Effacer TOUTES les zones a flouter deja placees ?")) return;
  state = CARDS.map(() => []);
  saveState();
  render();
}

function applyFilter(){
  const q = document.getElementById("search").value.toLowerCase();
  const onlyTodo = document.getElementById("onlyTodo").checked;
  const cards = document.getElementById("grid").children;
  for(const card of cards){
    const matchesSearch = !q || card.dataset.name.includes(q);
    const matchesTodo = !onlyTodo || card.dataset.todo === "1";
    card.classList.toggle("hidden", !(matchesSearch && matchesTodo));
  }
}

function exportAll(){
  const out = {};
  CARDS.forEach((car, idx) => {
    if(state[idx].length > 0){
      out[car.url] = state[idx].map(b => [
        Math.round(b.x * 10) / 10,
        Math.round(b.y * 10) / 10,
        Math.round(b.w * 10) / 10,
        Math.round(b.h * 10) / 10
      ]);
    }
  });
  const count = Object.keys(out).length;
  document.getElementById("exportLabel").textContent = count + " photo(s) avec des zones a flouter - donne ce bloc a Claude :";
  document.getElementById("exportText").value = JSON.stringify(out, null, 2);
  document.getElementById("exportPanel").style.display = "block";
  document.getElementById("exportPanel").scrollIntoView({behavior:"smooth"});
}

render();
</script>
</body>
</html>
"""

HTML = HTML.replace("__CARDS_JSON__", CARDS_JSON)

out_path = os.path.join(BASE, "..", "www", "blur-editor.html")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(HTML)
print("Wrote", out_path, "-", len(CARDS), "cars")
