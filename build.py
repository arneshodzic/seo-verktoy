# -*- coding: utf-8 -*-
"""Bygger hub-siden (index.html) ved å scanne verktoy/*/ mappene.
Kjøres av cron-botten etter hver publisering."""
import os, json, re

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, "verktoy")

def extract(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        t = f.read()
    def grab(pat):
        m = re.search(pat, t)
        return m.group(1).strip() if m else ""
    title = grab(r"<title>(.*?)</title>")
    # visningsnavn = tittel før skilletegn
    name = re.split(r"\s*[|–-]\s*", title)[0]
    desc = grab(r'<meta name="description" content="(.*?)"')
    icon = grab(r"<h1>(.*?)</h1>") or "🔧"
    return {"name": name, "desc": desc, "icon": icon,
            "url": "verktoy/" + os.path.basename(os.path.dirname(meta_path)) + "/"}

tools = sorted(extract(os.path.join(d, "index.html"))
               for d in [os.path.join(TOOLS_DIR, x) for x in os.listdir(TOOLS_DIR)]
               if os.path.isfile(os.path.join(d, "index.html")))

cards = "\n".join(
    f'<a class="t" href="{t["url"]}"><span class="i">{t["icon"]}</span>'
    f'<span class="n">{t["name"]}</span><span class="d">{t["desc"]}</span></a>'
    for t in tools) or '<p>Ingen verktøy ennå.</p>'

html = f"""<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nettverktøy – gratis kalkulatorer og verktøy på norsk</title>
<meta name="description" content="Gratis norske nettverktøy: kalkulatorer, konvertere og hjelpemidler. Ingen registrering, ingen reklame.">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;line-height:1.6;padding:2rem 1rem}}
.wrap{{max-width:760px;margin:0 auto}}
h1{{color:#fff;font-size:1.9rem;margin-bottom:.3rem}}
p.sub{{color:#94a3b8;margin-bottom:1.5rem}}
.t{{display:flex;gap:1rem;align-items:flex-start;background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1rem;margin-bottom:.75rem;text-decoration:none;transition:border-color .15s}}
.t:hover{{border-color:#38bdf8}}
.i{{font-size:1.6rem}}
.n{{color:#fff;font-weight:600;display:block}}
.d{{color:#94a3b8;font-size:.9rem;display:block}}
footer{{margin-top:2rem;color:#64748b;font-size:.85rem;text-align:center}}
</style>
</head>
<body><div class="wrap">
<h1>🧰 Nettverktøy</h1>
<p class="sub">Gratis verktøy på norsk · {len(tools)} verktøy · bygget automatisk</p>
{cards}
<footer>Alle verktøy er gratis og krever ingen registrering.</footer>
</div></body></html>"""

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Hub bygget med {len(tools)} verktøy: {[t['name'] for t in tools]}")
