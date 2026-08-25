import footer
# -*- coding: utf-8 -*-
"""Bygger hub-siden (index.html) med kategorifaner.
Skanner verktoy/*/index.html, henter kat/navn/desc/icon fra generer.py sitt LIB."""
import os, re, sys, json

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
    desc = grab(r'<meta name="description" content="(.*?)"')
    folder = os.path.basename(os.path.dirname(meta_path))
    spec = LIB.get(folder, {})
    # navnet fra LIB er alltid riktig; fra title deler vi bare pa separator med
    # mellomrom rundt, ellers ryker "BMI-kalkulator" og "Rentes rente-kalkulator"
    name = spec.get("navn") or re.split(r"\s+[|–—-]\s+", title)[0].strip()
    # verktøy utenfor LIB: hent ikon fra h1 uten markup, bare første symbol
    h1 = re.sub(r"<[^>]+>", " ", grab(r"<h1>(.*?)</h1>")).split()
    icon = spec.get("icon") or (h1[0] if h1 else "\U0001f527")
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
    forste = not panels_html
    kort = "\n".join(
        f'<a class="t" data-sok="{(t["name"] + " " + t["desc"]).lower()}" href="{t["url"]}">'
        f'<span class="i" aria-hidden="true">{t["icon"]}</span>'
        f'<span class="n">{t["name"]}</span><span class="d">{t["desc"]}</span></a>'
        for t in grupper[kat])
    panels_html += (f'<div class="panel" id="p-{kat}" role="tabpanel" aria-labelledby="f-{kat}"'
                    f'{"" if forste else " hidden"}>\n{kort}\n</div>\n')

tabbtns = "".join(
    f'<button class="fane{" aktiv" if i == 0 else ""}" id="f-{kat}" data-kat="{kat}" type="button" '
    f'role="tab" aria-controls="p-{kat}" aria-selected="{"true" if i == 0 else "false"}" '
    f'tabindex="{0 if i == 0 else -1}">{label}<span class="ant">{len(grupper[kat])}</span></button>\n'
    for i, (kat, label) in enumerate(k for k in KATEGORIER if k[0] in grupper))

# ItemList-schema av alle kalkulatorene (SEO)
BASE = "https://arneshodzic.github.io/seo-verktoy/"
schema = json.dumps({
    "@context": "https://schema.org", "@type": "CollectionPage",
    "name": "Smartkalkulator", "url": BASE, "inLanguage": "nb-NO",
    "description": "Gratis norske kalkulatorer for finans, bil, helse og hverdag.",
    "mainEntity": {"@type": "ItemList", "numberOfItems": len(tools),
                   "itemListElement": [
                       {"@type": "ListItem", "position": i + 1, "name": t["name"],
                        "url": BASE + t["url"]} for i, t in enumerate(tools)]},
}, ensure_ascii=False)

foot = footer.footer_html("Smartkalkulator",
    [(t["name"], t["url"]) for t in tools[:8]],
    root="")
html = """<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smartkalkulator – gratis kalkulatorer for finans, bil, helse og hverdag</title>
<meta name="description" content="Gratis norske kalkulatorer: moms, lån, feriepenger, kalorier, BMI, elbillading og mer. Raske svar, ingen registrering.">
<link rel="canonical" href="https://arneshodzic.github.io/seo-verktoy/">
<meta name="theme-color" content="#060a14">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Smartkalkulator">
<meta property="og:locale" content="nb_NO">
<meta property="og:title" content="Smartkalkulator – gratis kalkulatorer for finans, bil, helse og hverdag">
<meta property="og:description" content="Gratis norske kalkulatorer: moms, lån, feriepenger, kalorier, BMI, elbillading og mer. Raske svar, ingen registrering.">
<meta property="og:url" content="https://arneshodzic.github.io/seo-verktoy/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 96 96'%3E%3Cg transform='rotate(-7 48 48)'%3E%3Cpath d='M32 11h25.2L75 28.8V74a11 11 0 0 1-11 11H32a11 11 0 0 1-11-11V22a11 11 0 0 1 11-11z' fill='%23101a2c' stroke='%2322d3ee' stroke-width='4'/%3E%3Crect x='30' y='21.5' width='36' height='17' rx='4.5' fill='%2305202a' stroke='%2322d3ee' stroke-width='2.5'/%3E%3Cpath d='M13.6 2 4.9 14.4h5.5L8.6 22l8.9-12.6h-5.6z' transform='translate(41.4 24.2) scale(.56)' fill='%2367e8f9'/%3E%3Cg fill='%232b3a54'%3E%3Crect x='30' y='48' width='11' height='9' rx='2.5'/%3E%3Crect x='44' y='48' width='11' height='9' rx='2.5'/%3E%3Crect x='30' y='62' width='11' height='9' rx='2.5'/%3E%3C/g%3E%3Crect x='44' y='62' width='11' height='9' rx='2.5' fill='%2322d3ee'/%3E%3C/g%3E%3C/svg%3E">
<script type="application/ld+json">__SCHEMA__</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap">
<style>
:root{
  --bg:#060a14;--card-a:rgba(20,31,53,.92);--card-b:rgba(11,18,32,.94);
  --line:#1e2b44;--line-2:#31456a;
  --txt:#e9eefb;--mut:#a7b5cc;--dim:#8496af;
  --acc:#22d3ee;--acc-lys:#67e8f9;--acc-2:#818cf8;
  --r:16px;--r-s:12px;
  --skygge:0 1px 0 rgba(255,255,255,.045) inset,0 22px 44px -30px rgba(0,0,0,.95);
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:Inter,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--txt);
  line-height:1.65;font-size:16px;padding:0 1rem 3rem;overflow-x:hidden;-webkit-font-smoothing:antialiased}
body::before,body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none}
body::before{background:
  radial-gradient(920px 540px at 12% -12%,rgba(34,211,238,.19),transparent 62%),
  radial-gradient(780px 480px at 92% 0%,rgba(129,140,248,.16),transparent 64%),
  linear-gradient(180deg,#080f1e,#060a14 48%)}
body::after{opacity:.5;
  background-image:linear-gradient(rgba(150,185,255,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(150,185,255,.055) 1px,transparent 1px);
  background-size:58px 58px;
  -webkit-mask-image:radial-gradient(72% 52% at 50% 0%,#000,transparent);
          mask-image:radial-gradient(72% 52% at 50% 0%,#000,transparent)}
.wrap{

/* ---------- footer med kolonner ---------- */
.site-footer{margin-top:2.4rem;border-top:1px solid var(--line);
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent);
  padding:2.2rem 0 1.4rem}
.foot-grid{max-width:960px;margin:0 auto;padding:0 1rem;
  display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:1.6rem}
.brand-col .logo{justify-content:flex-start;font-size:1.3rem}
.brand-col p{color:var(--mut);font-size:.9rem;line-height:1.55;margin-top:.7rem;max-width:30ch}
.foot-h{font-family:Sora,Inter,sans-serif;font-weight:600;color:#fff;font-size:.82rem;
  letter-spacing:.04em;text-transform:uppercase;margin-bottom:.8rem}
.foot-col a{display:block;color:var(--mut);text-decoration:none;font-size:.9rem;
  padding:.28rem 0;transition:color .15s}
.foot-col a:hover{color:var(--acc-lys)}
.foot-bot{max-width:960px;margin:1.6rem auto 0;padding:1.1rem 1rem 0;border-top:1px solid var(--line);
  color:var(--dim);font-size:.8rem;text-align:center;line-height:1.6}
.foot-bot a{color:var(--dim)}
.foot-bot a:hover{color:var(--acc-lys)}
@media(max-width:680px){.foot-grid{grid-template-columns:1fr 1fr}}
@media(max-width:420px){.foot-grid{grid-template-columns:1fr}}
max-width:960px;margin:0 auto}
a{color:var(--acc-lys);text-underline-offset:3px}
:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:8px}
[hidden]{display:none!important}

/* ---------- hero ---------- */
header{padding:2.3rem 0 .7rem;text-align:center}
.logo{display:inline-flex;align-items:center;gap:.7rem;font-family:Sora,Inter,sans-serif;font-weight:700;
  font-size:clamp(1.7rem,7.4vw,2.5rem);letter-spacing:-.04em;color:#fff;line-height:1}
.logo svg{width:clamp(40px,11vw,54px);height:clamp(40px,11vw,54px);flex:0 0 auto;
  filter:drop-shadow(0 0 14px rgba(34,211,238,.5))}
.logo span{white-space:nowrap}
.logo i{font-style:normal;color:var(--acc)}
.slag{font-family:Sora,Inter,sans-serif;font-size:clamp(1.02rem,4.2vw,1.32rem);font-weight:600;color:#fff;
  margin-top:1.3rem;letter-spacing:-.02em}
.sub{color:var(--mut);margin-top:.45rem;font-size:.98rem}
.sub b{color:var(--acc-lys);font-weight:600}

/* ---------- kategorifaner ---------- */
.faner{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin:1.55rem 0 1.3rem}
.fane{display:inline-flex;align-items:center;gap:.45rem;font:inherit;font-size:.9rem;font-weight:500;
  color:var(--mut);background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:999px;
  padding:.52rem .95rem;cursor:pointer;transition:color .18s,border-color .18s,background .18s,transform .18s}
.fane:hover{color:#fff;border-color:var(--line-2);background:rgba(255,255,255,.06)}
.fane .ant{font-size:.72rem;font-weight:600;font-variant-numeric:tabular-nums;color:var(--dim);
  background:rgba(255,255,255,.07);border-radius:999px;padding:.05rem .42rem;transition:.18s}
.fane.aktiv{color:#04212b;font-weight:600;border-color:transparent;
  background:linear-gradient(180deg,#67e8f9,#22d3ee);box-shadow:0 12px 26px -14px rgba(34,211,238,.9)}
.fane.aktiv .ant{color:#04212b;background:rgba(4,33,43,.16)}

/* ---------- verktøykort ---------- */
.panel{display:grid;grid-template-columns:1fr;gap:.7rem}
@media(min-width:660px){.panel{grid-template-columns:1fr 1fr}}
.t{position:relative;display:grid;grid-template-columns:auto 1fr;grid-template-areas:"i n" "i d";
  column-gap:.9rem;row-gap:.15rem;align-items:start;text-decoration:none;overflow:hidden;
  background:linear-gradient(168deg,var(--card-a),var(--card-b));border:1px solid var(--line);
  border-radius:var(--r);padding:1.05rem 1.1rem;box-shadow:var(--skygge);
  animation:inn .38s both;transition:border-color .18s,transform .18s,box-shadow .18s}
.t::after{content:'';position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .22s;
  background:radial-gradient(420px 160px at 12% 0%,rgba(34,211,238,.13),transparent 70%)}
.t:hover,.t:focus-visible{border-color:rgba(34,211,238,.45);transform:translateY(-2px);
  box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 26px 44px -30px rgba(34,211,238,.75)}
.t:hover::after,.t:focus-visible::after{opacity:1}
.i{grid-area:i;width:2.6rem;height:2.6rem;display:grid;place-items:center;font-size:1.3rem;border-radius:14px;
  border:1px solid rgba(34,211,238,.28);background:linear-gradient(158deg,rgba(34,211,238,.19),rgba(129,140,248,.12));
  transition:box-shadow .22s}
.t:hover .i{box-shadow:0 0 22px -6px rgba(34,211,238,.7)}
.n{grid-area:n;font-family:Sora,Inter,sans-serif;font-weight:600;font-size:1.03rem;color:#fff;letter-spacing:-.02em}
.d{grid-area:d;color:var(--mut);font-size:.88rem;line-height:1.55;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}

/* ---------- bunn ---------- */
.info{margin-top:1.9rem;padding:1.2rem 1.25rem;border:1px solid var(--line);border-radius:var(--r);
  background:linear-gradient(120deg,rgba(34,211,238,.08),rgba(129,140,248,.06));color:var(--mut);font-size:.94rem}
.info strong{display:block;color:#fff;font-family:Sora,Inter,sans-serif;margin-bottom:.2rem}
footer{margin-top:1.7rem;padding-top:1.2rem;border-top:1px solid var(--line);color:var(--dim);
  font-size:.83rem;text-align:center}

@keyframes inn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
@media(max-width:400px){body{padding:0 .8rem 2.5rem}.t{padding:.9rem}.fane{padding:.48rem .8rem;font-size:.85rem}}
.sokefelt{position:relative;max-width:520px;margin:1.4rem auto 0}
.sokefelt input{width:100%;padding:.85rem 1.1rem .85rem 2.9rem;font:inherit;font-size:1rem;
  color:#fff;background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:999px;
  transition:border-color .18s,box-shadow .18s}
.sokefelt input::placeholder{color:var(--dim)}
.sokefelt input:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px rgba(34,211,238,.18),0 0 26px -8px rgba(34,211,238,.5)}
.sokefelt .lupe{position:absolute;left:1.05rem;top:50%;transform:translateY(-50%);
  color:var(--dim);pointer-events:none;font-size:1rem}
.tomt{display:none;text-align:center;color:var(--mut);padding:2rem 1rem;border:1px dashed var(--line-2);
  border-radius:var(--r);margin-top:.7rem}
mark{background:rgba(34,211,238,.25);color:var(--acc-lys);border-radius:4px;padding:0 .1em}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="logo">
    <svg viewBox="0 0 96 96" aria-hidden="true" focusable="false">
      <g transform="rotate(-7 48 48)">
        <path d="M32 11h25.2L75 28.8V74a11 11 0 0 1-11 11H32a11 11 0 0 1-11-11V22a11 11 0 0 1 11-11z"
              fill="#111a2b" stroke="#22d3ee" stroke-width="3.2" stroke-linejoin="round"/>
        <rect x="30" y="21.5" width="36" height="17" rx="4.5" fill="#05202a" stroke="#22d3ee" stroke-width="2"/>
        <path d="M13.6 2 4.9 14.4h5.5L8.6 22l8.9-12.6h-5.6z" transform="translate(41.4 24.2) scale(.56)" fill="#67e8f9"/>
        <g fill="#2b3a54">
          <rect x="30" y="46" width="9.5" height="8" rx="2.4"/><rect x="43.2" y="46" width="9.5" height="8" rx="2.4"/>
          <rect x="56.5" y="46" width="9.5" height="8" rx="2.4"/><rect x="30" y="57.5" width="9.5" height="8" rx="2.4"/>
          <rect x="43.2" y="57.5" width="9.5" height="8" rx="2.4"/><rect x="56.5" y="57.5" width="9.5" height="8" rx="2.4"/>
          <rect x="30" y="69" width="9.5" height="8" rx="2.4"/><rect x="43.2" y="69" width="9.5" height="8" rx="2.4"/>
        </g>
        <rect x="56.5" y="69" width="9.5" height="8" rx="2.4" fill="#22d3ee"/>
      </g>
    </svg>
    <span>Smart<i>kalkulator</i></span>
  </div>
  <h1 class="slag">Regn ut svaret på sekunder</h1>
  <p class="sub"><b>__ANTALL__ gratis kalkulatorer</b> &middot; ingen registrering &middot; ingen sporing</p>
</header>

<div class="sokefelt">
  <span class="lupe" aria-hidden="true">🔍</span>
  <input type="search" id="sok" placeholder="Søk blant kalkulatorene – f.eks. «moms», «lån», «BMI»…"
         aria-label="Søk i kalkulatorer" autocomplete="off">
</div>

<nav class="faner" role="tablist" aria-label="Kategorier">
__FANER__
</nav>

<main>
__PANELS__
</main>

<div class="tomt" id="tomt-sok">Ingen kalkulatorer matcher søket 😕 Prøv et annet ord.</div>

<div class="info">
  <strong>Nye kalkulatorer hver uke</strong>
  Alle verktøyene er gratis, fungerer i nettleseren og lagrer ingenting. Vi bygger nye kalkulatorer
  fortløpende – finans, bil og reise, livsstil og helse, og praktisk hverdag.
</div>

__FOOTER__
</div>

<script>
(function(){
  var faner=[].slice.call(document.querySelectorAll('.fane'));
  function vis(fane){
    faner.forEach(function(f){
      var pa=(f===fane);
      f.classList.toggle('aktiv',pa);
      f.setAttribute('aria-selected',pa?'true':'false');
      f.tabIndex=pa?0:-1;
      var panel=document.getElementById('p-'+f.dataset.kat);
      if(panel){panel.hidden=!pa}
    });
  }
  faner.forEach(function(f,i){
    f.addEventListener('click',function(){vis(f)});
    f.addEventListener('keydown',function(e){
      var n=null;
      if(e.key==='ArrowRight'||e.key==='ArrowDown'){n=faner[(i+1)%faner.length]}
      else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){n=faner[(i-1+faner.length)%faner.length]}
      else if(e.key==='Home'){n=faner[0]}
      else if(e.key==='End'){n=faner[faner.length-1]}
      if(n){e.preventDefault();vis(n);n.focus()}
    });
  });

  /* ---------- søk over alle kalkulatorene ---------- */
  var sokInput=document.getElementById('sok');
  var kort=[].slice.call(document.querySelectorAll('.panel .t'));
  var tomBoks=document.getElementById('tomt-sok');
  function fjernMark(el){el.innerHTML=el.innerHTML.replace(/<\/?mark>/g,'')}
  sokInput.addEventListener('input',function(){
    var q=sokInput.value.trim().toLowerCase();
    kort.forEach(fjernMark);
    if(!q){
      kort.forEach(function(k){k.style.display=''});
      if(tomBoks)tomBoks.style.display='none';
      faner.forEach(function(f){f.style.display=''});
      return;
    }
    var synlige=0;
    kort.forEach(function(k){
      var treff=(k.getAttribute('data-sok')||'').indexOf(q)>-1;
      k.style.display=treff?'':'none';
      if(treff){synlige++;markOpp(k,q)}
    });
    if(tomBoks)tomBoks.style.display=synlige===0?'block':'none';
  });
  function markOpp(el,q){
    var walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null,false);
    var noder=[];while(walker.nextNode())noder.push(walker.currentNode);
    noder.forEach(function(node){
      var idx=node.textContent.toLowerCase().indexOf(q);
      if(idx>-1&&node.parentNode.nodeName!=='MARK'){
        var etter=node.splitText(idx);
        etter.splitText(q.length);
        var m=document.createElement('mark');
        m.appendChild(etter.cloneNode(true));
        node.parentNode.replaceChild(m,etter);
      }
    });
  }
})();
</script>
</body></html>"""

html = (html.replace("__SCHEMA__", schema)
            .replace("__ANTALL__", str(len(tools)))
            .replace("__FANER__", tabbtns)
            .replace("__PANELS__", panels_html)
            .replace("__FOOTER__", foot))
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Hub bygget: {len(tools)} verktøy i {len(grupper)} kategorier:",
      {k: len(v) for k, v in sorted(grupper.items())})
