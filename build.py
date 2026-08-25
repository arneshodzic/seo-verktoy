# -*- coding: utf-8 -*-
"""Bygger hub-siden (index.html) med kategorifaner.
Skanner verktoy/*/index.html, henter kat/navn/desc/icon fra generer.py sitt LIB."""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generer import LIB

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, "verktoy")

KATEGORIER = [
    ("finans", "💰 Finans"),
    ("bil", "🚗 Bil & reise"),
    ("livsstil", "💪 Livsstil & helse"),
    ("hverdag", "📅 Hverdag"),
    ("annet", "🔧 Annet"),
]

# verktøy som ikke ligger i LIB (håndlagde) får kategori her:
KAT_EKSTRA = {"bilkostnadskalkulator": "bil"}

def extract(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        t = f.read()
    def grab(pat):
        m = re.search(pat, t)
        return m.group(1).strip() if m else ""
    title = grab(r"<title>(.*?)</title>")
    name = re.split(r"\s*[|–-]\s*", title)[0]
    desc = grab(r'<meta name="description" content="(.*?)"')
    folder = os.path.basename(os.path.dirname(meta_path))
    spec = LIB.get(folder, {})
    icon = spec.get("icon", grab(r"<h1>(.*?)</h1>") or "🔧")
    return {"name": name, "desc": desc, "icon": icon,
            "kat": spec.get("kat", KAT_EKSTRA.get(folder, "annet")),
            "url": "verktoy/" + folder + "/"}

tools = [extract(os.path.join(TOOLS_DIR, x, "index.html"))
         for x in os.listdir(TOOLS_DIR)
         if os.path.isfile(os.path.join(TOOLS_DIR, x, "index.html"))]
tools.sort(key=lambda t: t["name"])

# grupper per kategori
grupper = {}
for t in tools:
    grupper.setdefault(t["kat"], []).append(t)

faner = ""
panels_html = ""
for i, (kat, label) in enumerate(KATEGORIER):
    if kat not in grupper:
        continue
    kort = "\n".join(
        f'<a class="t" href="{t["url"]}"><span class="i">{t["icon"]}</span>'
        f'<span class="n">{t["name"]}</span><span class="d">{t["desc"]}</span></a>'
        for t in grupper[kat])
    panels_html += f'<div class="panel" id="p-{kat}" style="display:{"block" if i == 0 else "none"}">\n{kort}\n</div>\n'

tabbtns = "".join(
    f'<button class="fane{"" if i == 0 else ""}" data-kat="{kat}" '
    f'style="{"border-color:#38bdf8;color:#fff" if i == 0 else ""}">{label}</button>\n'
    for i, (kat, label) in enumerate(KATEGORIER) if kat in grupper)

html = """<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smartkalkulator – gratis kalkulatorer for finans, bil, helse og hverdag</title>
<meta name="description" content="Gratis norske kalkulatorer: moms, lån, feriepenger, kalorier, BMI, elbillading og mer. Raske svar, ingen registrering.">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;line-height:1.6;padding:2rem 1rem}
.wrap{max-width:760px;margin:0 auto}
header{text-align:center;margin-bottom:1.5rem}
.logo{font-size:2rem;font-weight:800;color:#fff;letter-spacing:-.5px}
.logo span{color:#38bdf8}
p.sub{color:#94a3b8;margin-top:.3rem}
.faner{display:flex;gap:.5rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.25rem}
.fane{background:#1e293b;border:1px solid #334155;border-radius:999px;color:#94a3b8;
  padding:.5rem 1.1rem;font-size:.92rem;cursor:pointer;transition:all .15s}
.fane:hover{border-color:#38bdf8;color:#fff}
.panel .t{display:flex;gap:1rem;align-items:flex-start;background:#1e293b;border:1px solid #334155;
  border-radius:12px;padding:1rem;margin-bottom:.75rem;text-decoration:none;transition:border-color .15s}
.panel .t:hover{border-color:#38bdf8}
.i{font-size:1.6rem}
.n{color:#fff;font-weight:600;display:block}
.d{color:#94a3b8;font-size:.9rem;display:block}
footer{margin-top:2rem;color:#64748b;font-size:.85rem;text-align:center}
@media(max-width:480px){.logo{font-size:1.6rem}.fane{padding:.45rem .85rem;font-size:.85rem}}
</style>
</head>
<body><div class="wrap">
<header>
  <div class="logo">Smart<span>kalkulator</span></div>
  <p class="sub">__ANTALL__ gratis kalkulatorer · raske svar · ingen registrering</p>
</header>
<nav class="faner">
__FANER__
</nav>
__PANELS__
<footer>Alle kalkulatorene er gratis og krever ingen registrering.</footer>
</div>
<script>
document.querySelectorAll('.fane').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.fane').forEach(function(x){x.style.borderColor='#334155';x.style.color='#94a3b8'});
    b.style.borderColor='#38bdf8';b.style.color='#fff';
    document.querySelectorAll('.panel').forEach(function(p){p.style.display='none'});
    document.getElementById('p-'+b.dataset.kat).style.display='block';
  });
});
</script>
</body></html>"""

html = html.replace("__ANTALL__", str(len(tools))).replace("__FANER__", tabbtns).replace("__PANELS__", panels_html)
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Hub bygget: {len(tools)} verktøy i {len(grupper)} kategorier:",
      {k: len(v) for k, v in sorted(grupper.items())})
