import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

APP_TITLE = "Pondruff Preis Kalkulator"
LOGO_FILE = "logo.png"
ICON_FILE = "icon.png"
VAT_RATE = 19.0

# Quelle: „2018-04-21 EUROPL01 - für TiN +CrN + TiCN.xls“, Blatt „mm³ Tabelle“.
# Die Excel-Datei rechnet mit mm³-Schwellen und VLOOKUP(..., TRUE), also mit der
# jeweils nächstkleineren Staffel. Die Faktoren unten sind die finalen
# Beschichtungs-Multiplikatoren aus der Originalformel:
# CrN/TiCN = 1.2 * 1.1, TiN = 1.1.
COATING_FACTORS = {
    "TiCN": 1.32,
    "CrN": 1.32,
    "TiN": 1.10,
}

PRICE_TABLE = [
    [1000, 2.55645940598109], [2000, 1.27822970299055],
    [3000, 0.971454574272815], [6000, 0.843631603973761],
    [10000, 0.81806700991395], [15000, 0.766937821794328],
    [20000, 0.715808633674706], [25000, 0.664679445555084],
    [30000, 0.613550257435462], [40000, 0.511291881196219],
    [50000, 0.460162693076597], [60000, 0.429485180204824],
    [70000, 0.409033504956975], [80000, 0.342565560401466],
    [150000, 0.32722680396558], [200000, 0.306775128717731],
    [250000, 0.301662209905769], [300000, 0.296549291093807],
    [400000, 0.291436372281845], [500000, 0.28121053465792],
    [600000, 0.270984697033996], [700000, 0.265871778222034],
    [800000, 0.245420102974185], [900000, 0.235194265350261],
    [950000, 0.230081346538298], [1000000, 0.214742590102412],
    [1100000, 0.199403833666525], [1200000, 0.189177996042601],
    [1300000, 0.178952158418676], [1400000, 0.168726320794752],
    [1500000, 0.16361340198279], [1600000, 0.153387564358866],
    [1700000, 0.143161726734941], [1800000, 0.138048807922979],
    [1900000, 0.132935889111017], [2000000, 0.11759713267513],
    [2500000, 0.102258376239244], [3000000, 0.0971454574272815],
    [3500000, 0.0869196198033572], [4000000, 0.081806700991395],
    [4500000, 0.0766937821794328], [5000000, 0.0715808633674706],
    [6500000, 0.0664679445555084], [7500000, 0.0613550257435462],
    [10000000, 0.056242106931584], [35000000, 0.0511291881196219],
]


def img_data_uri(path: str) -> str:
    file = Path(path)
    if not file.exists():
        return ""
    suffix = file.suffix.lower().replace(".", "")
    mime = "jpeg" if suffix in ["jpg", "jpeg"] else "png"
    encoded = base64.b64encode(file.read_bytes()).decode("utf-8")
    return f"data:image/{mime};base64,{encoded}"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=ICON_FILE,
    layout="wide",
    initial_sidebar_state="collapsed",
)

logo_uri = img_data_uri(LOGO_FILE)
icon_uri = img_data_uri(ICON_FILE)
coatings_json = json.dumps(COATING_FACTORS, ensure_ascii=False)
price_table_json = json.dumps(PRICE_TABLE)

html = f"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
<title>{APP_TITLE}</title>
<style>
:root {{
  --bg:#0b0e14;
  --panel:#171c25;
  --panel2:#202633;
  --red:#e53935;
  --redDark:#b71c1c;
  --redSoft:#ff6b6b;
  --muted:#aeb7c5;
  --border:#3b465a;
}}
* {{ box-sizing:border-box; }}
html, body {{ margin:0; padding:0; background:#0b0e14; color:white; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif; }}
body {{
  background:
    radial-gradient(circle at top left, rgba(229,57,53,.22), transparent 30%),
    radial-gradient(circle at bottom right, rgba(48,55,70,.55), transparent 32%),
    linear-gradient(180deg,#0b0e14 0%,#10141c 100%);
}}
.app {{ max-width:460px; margin:0 auto; padding:18px 16px 70px; }}
.logo {{ display:block; width:100%; max-width:380px; margin:8px auto 24px; border-radius:16px; filter:drop-shadow(0 20px 36px rgba(0,0,0,.48)); }}
.title {{ text-align:center; font-size:36px; line-height:1.03; font-weight:950; letter-spacing:-.045em; margin:0; }}
.title .red {{ color:var(--redSoft); }}
.subtitle {{ text-align:center; color:var(--muted); font-size:16px; line-height:1.5; margin:16px auto 24px; }}
.notice {{ background:rgba(24,48,76,.88); border:1px solid rgba(99,164,255,.25); border-radius:18px; padding:16px 18px; margin-bottom:18px; font-weight:750; line-height:1.55; box-shadow:0 12px 26px rgba(0,0,0,.18); }}
.card {{ background:linear-gradient(180deg,rgba(29,35,48,.98),rgba(14,18,27,.98)); border:1px solid rgba(85,97,122,.55); border-radius:22px; padding:18px; margin-bottom:18px; box-shadow:0 18px 36px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04); }}
.card-title {{ display:flex; align-items:center; gap:10px; font-size:19px; font-weight:900; margin-bottom:14px; }}
.card-title .icon {{ color:var(--redSoft); font-size:22px; }}
.muted {{ color:var(--muted); }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; width:100%; }}
.field {{ margin-bottom:14px; min-width:0; }}
label {{ display:block; margin-bottom:8px; font-size:14px; font-weight:650; color:#fff; }}
input, select {{ width:100%; min-width:0; height:48px; background:#151922; color:white; border:1px solid #343d50; border-radius:12px; padding:0 11px; font-size:15px; outline:none; }}
input:focus, select:focus {{ border-color:var(--redSoft); box-shadow:0 0 0 2px rgba(229,57,53,.18); }}
input[readonly] {{ opacity:.95; }}
.price-box {{ background:linear-gradient(135deg,#171c26,#222938); border:1px solid #3b465a; border-radius:16px; padding:14px 16px; margin-top:4px; color:var(--redSoft); font-weight:900; font-size:16px; line-height:1.55; }}
.btn {{ width:100%; min-height:52px; border:1px solid #3d4658; border-radius:14px; color:white; background:#2d3443; font-weight:900; font-size:16px; padding:12px 14px; cursor:pointer; }}
.btn.red {{ background:linear-gradient(135deg,var(--red),var(--redDark)); border-color:var(--red); }}
.btn-row {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }}
.position {{ border-bottom:1px solid rgba(255,255,255,.08); padding:14px 0; }}
.position-head {{ display:flex; justify-content:space-between; gap:12px; align-items:center; font-weight:900; font-size:16px; }}
.badge {{ display:inline-flex; align-items:center; justify-content:center; min-width:28px; height:28px; padding:0 8px; border-radius:8px; background:linear-gradient(135deg,var(--red),var(--redDark)); color:white; font-weight:900; margin-right:8px; }}
.pos-detail {{ color:var(--muted); font-size:14px; line-height:1.5; margin:7px 0 0 42px; }}
.delete {{ margin-top:10px; border-color:rgba(229,57,53,.5); color:#fff; }}
.total-card {{ position:relative; overflow:hidden; background:linear-gradient(135deg,#232a38,#151a24); border:1px solid rgba(99,112,140,.65); border-radius:24px; padding:24px; margin:26px 0 18px; box-shadow:0 22px 42px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.05); }}
.total-icons {{ position:absolute; right:16px; top:16px; display:flex; gap:8px; align-items:center; }}
.total-icons img {{ width:52px; height:52px; object-fit:cover; border-radius:14px; box-shadow:0 8px 20px rgba(0,0,0,.35); }}
.calculator-svg {{ width:56px; height:56px; filter:drop-shadow(0 8px 15px rgba(0,0,0,.35)); }}
.total-big {{ font-size:48px; font-weight:950; line-height:1.05; margin:8px 0 18px; }}
.total-line {{ display:flex; justify-content:space-between; gap:12px; border-top:1px solid rgba(255,255,255,.08); padding-top:10px; margin-top:10px; font-size:16px; }}
.gross {{ color:var(--redSoft); font-weight:950; font-size:18px; }}
.copybox {{ white-space:pre-wrap; background:#0f131b; color:#d6dbe4; border:1px solid #343d50; border-radius:14px; padding:14px; font-size:13px; line-height:1.45; margin-top:12px; display:none; }}
.caption {{ color:var(--muted); font-size:13px; line-height:1.45; margin-top:12px; }}
@media (min-width:900px) {{ .app {{ max-width:980px; }} .logo {{ max-width:620px; }} .desktop-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }} }}
</style>
</head>
<body>
<div class="app">
  {f'<img src="{logo_uri}" class="logo" alt="Pondruff Logo" />' if logo_uri else '<div class="notice">Logo nicht gefunden: logo.png</div>'}
  <h1 class="title">Pondruff<br><span class="red">Preis Kalkulator</span></h1>
  <p class="subtitle">Beschichtung auswählen, Maße eingeben und den Preis inklusive Rabatt direkt beim Kunden berechnen.</p>
  <div class="notice">ⓘ Jede Position hat eine eigene Schicht-Auswahl, Rabatt, Stückzahl und Notiz. Der Gesamtpreis wird automatisch berechnet.</div>

  <div class="card">
    <div class="card-title"><span class="icon">👥</span>Kunde & Notizen</div>
    <div class="field"><label>Kundenname (optional)</label><input id="customer" placeholder="Kundenname" /></div>
    <div class="field"><label>Notizen / Projekt (optional)</label><input id="project" placeholder="Notizen / Projekt" /></div>
  </div>

  <div class="card">
    <div class="card-title"><span class="icon">⚙️</span>Einstellungen</div>
    <div class="grid2">
      <div class="field"><label>Express-Aufschlag</label><select id="expressEnabled"><option value="no">Nein</option><option value="yes">Ja</option></select></div>
      <div class="field"><label>Express %</label><input id="expressPercent" inputmode="decimal" placeholder="z. B. 20" /></div>
    </div>
  </div>

  <div class="desktop-grid">
    <div class="card">
      <div class="card-title"><span class="icon">▣</span>Eckige Bauteile</div>
      <p class="muted">Schicht × Faktor × Breite A × Breite B × Höhe</p>
      <div class="grid2">
        <div class="field"><label>Schicht</label><select id="rectCoating"></select></div>
        <div class="field"><label>Faktor</label><input id="rectFactor" readonly /></div>
        <div class="field"><label>Breite A (mm)</label><input id="rectA" inputmode="decimal" /></div>
        <div class="field"><label>Breite B (mm)</label><input id="rectB" inputmode="decimal" /></div>
        <div class="field"><label>Höhe (mm)</label><input id="rectH" inputmode="decimal" /></div>
        <div class="field"><label>Stückzahl</label><input id="rectQty" inputmode="numeric" /></div>
        <div class="field"><label>Rabatt %</label><input id="rectDiscount" inputmode="decimal" /></div>
        <div class="field"><label>Notiz</label><input id="rectNote" placeholder="z. B. Fräser" /></div>
      </div>
      <div id="rectPreview" class="price-box">Normalpreis: 0,00 €<br>Rabatt: -0%<br>Preis nach Rabatt: 0,00 €</div>
      <button class="btn red" onclick="addRect()">+ Eckige Position hinzufügen</button>
    </div>

    <div class="card">
      <div class="card-title"><span class="icon">●</span>Runde Bauteile</div>
      <p class="muted">Schicht × Faktor × Durchmesser × Länge</p>
      <div class="grid2">
        <div class="field"><label>Schicht</label><select id="roundCoating"></select></div>
        <div class="field"><label>Faktor</label><input id="roundFactor" readonly /></div>
        <div class="field"><label>Durchmesser (mm)</label><input id="roundD" inputmode="decimal" /></div>
        <div class="field"><label>Länge (mm)</label><input id="roundL" inputmode="decimal" /></div>
        <div class="field"><label>Stückzahl</label><input id="roundQty" inputmode="numeric" /></div>
        <div class="field"><label>Rabatt %</label><input id="roundDiscount" inputmode="decimal" /></div>
      </div>
      <div class="field"><label>Notiz</label><input id="roundNote" placeholder="z. B. Bohrer" /></div>
      <div id="roundPreview" class="price-box">Normalpreis: 0,00 €<br>Rabatt: -0%<br>Preis nach Rabatt: 0,00 €</div>
      <button class="btn red" onclick="addRound()">+ Runde Position hinzufügen</button>
    </div>
  </div>

  <div class="card">
    <div class="card-title"><span class="icon">☰</span><span id="posTitle">Positionen (0)</span></div>
    <div id="positions"><p class="muted">Noch keine Positionen hinzugefügt.</p></div>
  </div>

  <div class="total-card">
    <div class="total-icons">
      <svg class='calculator-svg' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>
        <rect x='18' y='8' width='64' height='84' rx='10' fill='#303743' stroke='#666f7e' stroke-width='3'/>
        <rect x='27' y='17' width='46' height='18' rx='4' fill='#c8d5cf'/>
        <rect x='28' y='46' width='12' height='12' rx='3' fill='#ff6b6b'/><rect x='44' y='46' width='12' height='12' rx='3' fill='#ff6b6b'/><rect x='60' y='46' width='12' height='12' rx='3' fill='#ff6b6b'/>
        <rect x='28' y='63' width='12' height='12' rx='3' fill='#ff6b6b'/><rect x='44' y='63' width='12' height='12' rx='3' fill='#ff6b6b'/><rect x='60' y='63' width='12' height='12' rx='3' fill='#ff6b6b'/>
      </svg>
      {f'<img src="{icon_uri}" alt="Pondruff Icon" />' if icon_uri else ''}
    </div>
    <div class="muted">Gesamtpreis nach Rabatt</div>
    <div id="totalNetBig" class="total-big">0,00 €</div>
    <div class="total-line"><span>Normalpreis netto:</span><b id="normalSum">0,00 €</b></div>
    <div class="total-line"><span>Rabatt gesamt:</span><b id="discountSum">-0,00 €</b></div>
    <div class="total-line"><span>Express-Aufschlag:</span><b id="expressAmount">0,00 €</b></div>
    <div class="total-line"><span>MwSt. ({VAT_RATE:g}%):</span><b id="vatAmount">0,00 €</b></div>
    <div class="total-line gross"><span>Gesamtpreis brutto:</span><span id="totalGross">0,00 €</span></div>
  </div>

  <div class="btn-row">
    <button class="btn" onclick="resetAll()">↻ Zurücksetzen</button>
    <button class="btn red" onclick="copySummary()">📋 Ergebnis kopieren</button>
  </div>
  <div id="copyBox" class="copybox"></div>
  <div class="caption">Hinweis: Preise bitte vor verbindlichem Angebot intern prüfen. Dieses Tool dient als schnelle Kalkulationshilfe beim Kunden.</div>
</div>

<script>
const COATINGS = {coatings_json};
const PRICE_TABLE = {price_table_json};
const VAT_RATE = {VAT_RATE};
let positions = [];

function el(id) {{ return document.getElementById(id); }}
function parseNumber(v) {{
  if (v === null || v === undefined) return 0;
  v = String(v).trim();
  if (!v) return 0;
  v = v.replace(/\./g, '').replace(',', '.');
  const n = Number(v);
  return isNaN(n) ? 0 : n;
}}
function parseQty(v) {{ const n = Math.floor(parseNumber(v)); return n > 0 ? n : 1; }}
function euro(v) {{ return Number(v).toLocaleString('de-DE', {{minimumFractionDigits:2, maximumFractionDigits:2}}) + ' €'; }}
function factorText(v) {{ return v ? String(v).replace('.', ',') : ''; }}
function lookupRate(volume) {{
  if (volume <= 0) return 0;
  let rate = PRICE_TABLE[0][1];
  for (const row of PRICE_TABLE) {{
    if (volume >= row[0]) rate = row[1];
    else break;
  }}
  return rate;
}}
function roundUp(value, decimals=1) {{
  const f = Math.pow(10, decimals);
  return Math.ceil((Number(value) || 0) * f - 1e-9) / f;
}}
function calcPrice(volume, factor) {{
  if (volume <= 0 || factor <= 0) return 0;
  return lookupRate(volume) * volume / 1000 * factor;
}}
function discountPrice(price, discount) {{ discount = Math.max(0, Math.min(100, discount)); return Math.round(price * (1 - discount/100) * 100) / 100; }}
function coatingOptions(select) {{
  select.innerHTML = '<option>Bitte wählen</option>' + Object.keys(COATINGS).map(k => `<option>${{k}}</option>`).join('');
}}
function updateFactors() {{
  el('rectFactor').value = factorText(COATINGS[el('rectCoating').value] || 0);
  el('roundFactor').value = factorText(COATINGS[el('roundCoating').value] || 0);
}}
function rectCalc() {{
  const factor = COATINGS[el('rectCoating').value] || 0;
  const volume = parseNumber(el('rectA').value) * parseNumber(el('rectB').value) * parseNumber(el('rectH').value);
  const normal = roundUp(calcPrice(volume, factor) * parseQty(el('rectQty').value), 1);
  const discount = parseNumber(el('rectDiscount').value);
  const final = discountPrice(normal, discount);
  el('rectPreview').innerHTML = `Normalpreis: ${{euro(normal)}}<br>Rabatt: -${{discount}}%<br>Preis nach Rabatt: ${{euro(final)}}`;
  return {{normal, final, discount, factor}};
}}
function roundCalc() {{
  const factor = COATINGS[el('roundCoating').value] || 0;
  const d = parseNumber(el('roundD').value);
  const l = parseNumber(el('roundL').value);
  const volume = (d*d) * 3.1415 / 4 * l;
  const normal = roundUp(calcPrice(volume, factor) * parseQty(el('roundQty').value), 1);
  const discount = parseNumber(el('roundDiscount').value);
  const final = discountPrice(normal, discount);
  el('roundPreview').innerHTML = `Normalpreis: ${{euro(normal)}}<br>Rabatt: -${{discount}}%<br>Preis nach Rabatt: ${{euro(final)}}`;
  return {{normal, final, discount, factor}};
}}
function addRect() {{
  const c = rectCalc();
  const a = parseNumber(el('rectA').value), b = parseNumber(el('rectB').value), h = parseNumber(el('rectH').value);
  positions.push({{type:'Eckige Bauteile', coating: el('rectCoating').value, factor:c.factor, discount:c.discount, qty:parseQty(el('rectQty').value), normal:c.normal, final:c.final, details:`A: ${{a}} mm · B: ${{b}} mm · H: ${{h}} mm`, note:el('rectNote').value.trim()}});
  render();
}}
function addRound() {{
  const c = roundCalc();
  const d = parseNumber(el('roundD').value), l = parseNumber(el('roundL').value);
  positions.push({{type:'Runde Bauteile', coating: el('roundCoating').value, factor:c.factor, discount:c.discount, qty:parseQty(el('roundQty').value), normal:c.normal, final:c.final, details:`Durchmesser: ${{d}} mm · Länge: ${{l}} mm`, note:el('roundNote').value.trim()}});
  render();
}}
function delPos(i) {{ positions.splice(i,1); render(); }}
function render() {{
  el('posTitle').textContent = `Positionen (${{positions.length}})`;
  if (!positions.length) el('positions').innerHTML = '<p class="muted">Noch keine Positionen hinzugefügt.</p>';
  else el('positions').innerHTML = positions.map((p,i) => `<div class="position"><div class="position-head"><div><span class="badge">${{i+1}}</span>${{p.type}}</div><div>${{euro(p.final)}}</div></div><div class="pos-detail">${{p.coating}} · Faktor ${{factorText(p.factor)}}<br>${{p.details}}<br>Stk: ${{p.qty}} · Rabatt: ${{p.discount}}%${{p.note ? '<br><i>'+p.note+'</i>' : ''}}</div><button class="btn delete" onclick="delPos(${{i}})">✕ Position ${{i+1}} löschen</button></div>`).join('');
  const normal = positions.reduce((s,p)=>s+p.normal,0);
  const discounted = positions.reduce((s,p)=>s+p.final,0);
  const discount = normal - discounted;
  const expressPct = parseNumber(el('expressPercent').value);
  const express = el('expressEnabled').value === 'yes' ? discounted * expressPct/100 : 0;
  const net = Math.round((discounted + express) * 100)/100;
  const vat = Math.round(net * VAT_RATE)/100;
  const gross = Math.round((net + vat) * 100)/100;
  el('totalNetBig').textContent = euro(net);
  el('normalSum').textContent = euro(normal);
  el('discountSum').textContent = '-' + euro(discount);
  el('expressAmount').textContent = euro(express);
  el('vatAmount').textContent = euro(vat);
  el('totalGross').textContent = euro(gross);
}}
function resetAll() {{ positions = []; document.querySelectorAll('input').forEach(i => i.value=''); el('rectCoating').value='Bitte wählen'; el('roundCoating').value='Bitte wählen'; el('expressEnabled').value='no'; updateFactors(); rectCalc(); roundCalc(); render(); }}
function summaryText() {{
  const normal = positions.reduce((s,p)=>s+p.normal,0), discounted = positions.reduce((s,p)=>s+p.final,0);
  const expressPct = parseNumber(el('expressPercent').value);
  const express = el('expressEnabled').value === 'yes' ? discounted * expressPct/100 : 0;
  const net = Math.round((discounted + express)*100)/100;
  const vat = Math.round(net*VAT_RATE)/100, gross = Math.round((net+vat)*100)/100;
  let txt = `Pondruff Preis Kalkulator\nKunde: ${{el('customer').value}}\nNotiz/Projekt: ${{el('project').value}}\n\nPositionen:\n`;
  positions.forEach((p,i)=> txt += `${{i+1}}. ${{p.type}} | ${{p.coating}} | Faktor ${{factorText(p.factor)}} | ${{p.details}} | Stk: ${{p.qty}} | Rabatt: ${{p.discount}}% | Preis netto: ${{euro(p.final)}}${{p.note ? ' | '+p.note : ''}}\n`);
  txt += `\nGesamt netto: ${{euro(net)}}\nMwSt. (${{VAT_RATE}}%): ${{euro(vat)}}\nGesamt brutto: ${{euro(gross)}}`;
  return txt;
}}
async function copySummary() {{
  const txt = summaryText();
  el('copyBox').style.display='block'; el('copyBox').textContent = txt;
  try {{ await navigator.clipboard.writeText(txt); alert('Ergebnis wurde kopiert.'); }} catch(e) {{ alert('Kopieren nicht möglich. Text wird unten angezeigt.'); }}
}}
['rectCoating','roundCoating'].forEach(id => el(id).addEventListener('change', () => {{ updateFactors(); rectCalc(); roundCalc(); }}));
document.querySelectorAll('input, select').forEach(x => x.addEventListener('input', () => {{ updateFactors(); rectCalc(); roundCalc(); render(); }}));
coatingOptions(el('rectCoating')); coatingOptions(el('roundCoating')); updateFactors(); rectCalc(); roundCalc(); render();
</script>
</body>
</html>
"""

# Wichtig: scrolling=False verhindert den zweiten Scrollbalken auf dem iPhone.
# Die Höhe ist bewusst groß gewählt, damit die Seite normal über Safari/Streamlit scrollt.
components.html(html, height=6500, scrolling=False)

