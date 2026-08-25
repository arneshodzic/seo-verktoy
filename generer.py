# -*- coding: utf-8 -*-
"""Verktøyfabrikk: genererer verktøysider fra innebygd bibliotek.
Bruk:
  python generer.py --test <nokkel>   # rendrer til tmp/ uten å røre kø/logg
  python generer.py --publiser       # tar første ledige fra ko.txt, bygger, stryker, logger, oppdaterer hub
"""
import os, sys, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(ROOT, "tmp")

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- bibliotek
# js har tilgang til: g(id)=parseFloat, gs(id)=rå streng,
# fmtK(n)=avrundet kr, n0(n)=heltall, n1(n)=1 desimal komma
LIB = {
    "moms-kalkulator": {
        "navn": "Momskalkulator", "icon": "🧾",
        "tittel": "Momskalkulator – legg til eller fjern 25 % mva | Nettverktøy",
        "desc": "Gratis momskalkulator: legg til eller fjern moms (mva) 25 %, 15 % eller 12 % på sekunder. Se beløp med og uten moms.",
        "intro": "Regn ut moms raskt: legg moms til et nettobeløp, eller finn netto- og momsandelen fra et bruttobeløp.",
        "selects": [("retning", "Hva vil du gjøre?", [
            ["leggtil", "Legge moms til beløpet"],
            ["fjern", "Fjerne moms (finne beløpet uten moms)"]], "leggtil")],
        "inputs": [("belop", "Beløp (kr)", "10000", "number"),
                   ("sats", "Momssats (%)", "25", "number")],
        "js": """var ret=gs('retning'), s=g('sats')/100, b=g('belop'), m, um, mm;
if(ret==='leggtil'){ um=b; mm=b*(1+s); m=mm-um; } else { mm=b; um=b/(1+s); m=mm-um; }
return {stor: fmtK(m), sub:'i moms ('+gs('sats')+' %)',
  celler:[['Uten moms',fmtK(um)],['Med moms',fmtK(mm)]],
  rader:[['Grunnlag uten moms',fmtK(um)],['Moms '+n1(s*100)+' %',fmtK(m)],['Sum med moms',fmtK(mm)]]};""",
        "faq": [
            ["Hvor mye er moms i Norge?", "Alminnelig momssats er 25 %. Mat og drikke på flaskke har 15 %, og noen tjenester som persontransport og kinobilletter har 12 %."],
            ["Hvordan regner jeg moms baklengs?", "Del bruttobeløpet på 1,25 (ved 25 % sats). Da får du beløpet uten moms. Momsen er differansen. Kalkulatoren gjør dette automatisk."],
            ["Er momsdetaljene gyldige for regnskap?", "Kalkulatoren er et hjelpeverktøy. Bruk alltid faktura og regnskapsprogrammet ditt for offisielle tall."]]},

    "laanekalkulator": {
        "navn": "Lånekalkulator", "icon": "🏦",
        "tittel": "Lånekalkulator – regn ut terminbeløp og total rente | Nettverktøy",
        "desc": "Gratis lånekalkulator: se månedlig terminbeløp, totalkostnad og total rente for lån med annuitet. Rask og enkel.",
        "intro": "Se hva lånet koster deg: terminbeløp per måned, total rentekostnad og totalt betalt over hele løpetiden.",
        "inputs": [("belop", "Lånebeløp (kr)", "300000", "number"),
                   ("rente", "Nominell rente (% per år)", "5.2", "number"),
                   ("aar", "Løpetid (år)", "10", "number")],
        "js": """var b=g('belop'), r=g('rente')/100/12, n=g('aar')*12;
var t = r>0 ? b*r/(1-Math.pow(1+r,-n)) : b/n;
var tot=t*n, rente=tot-b;
return {stor: fmtK(t), sub:'per måned',
  celler:[['Antall terminer',n0(n)],['Total rente',fmtK(rente)]],
  rader:[['Terminbeløp',fmtK(t)+' / mnd'],['Totalt betalt',fmtK(tot)],['Rentekostnad',fmtK(rente)],['Effektiv rente ca.',n1((Math.pow(1+g('rente')/100/12,12)-1)*100)+' %']]}""",
        "faq": [
            ["Hvordan regnes terminbeløpet ut?", "Kalkulatoren bruker annuitetslån: likt terminbeløp hver måned gjennom hele løpetiden, der renteandelen synser og avdragsgjelden øker over tid."],
            ["Hva er forskjellen på nominell og effektiv rente?", "Den nominelle renten er selve lånerenten. Den effektive inkluderer også gebyrer og etableringskostnad, og er derfor høyere. Kalkulatoren viser effektiv rente uten gebyrer."],
            ["Lønner det seg å betale ned raskere?", "Som regel ja – hver ekstra krone du betaler ned reduserer rentekostnaden for resten av løpetiden. Prøv å kutte løpetiden og se hvordan total rente faller."]]},

    "kaloriberegner": {
        "navn": "Kaloriberegner", "icon": "🔥",
        "tittel": "Kaloriberegner – ditt daglige kaloriebehov | Nettverktøy",
        "desc": "Finn ditt daglige kaloriebehov gratis: BMR og forbrenning basert på kjønn, alder, vekt, høyde og aktivitetsnivå.",
        "intro": "Basert på Mifflin-St Jeor-formelen: først hvileforbrenning (BMR), så daglig behov med aktivitetsnivået ditt.",
        "selects": [("kjonn", "Kjønn", [["mann", "Mann"], ["kvinne", "Kvinne"]], "mann"),
                    ("aktivitet", "Aktivitetsnivå", [
                        ["1.2", "Stillesittende (lite trening)"],
                        ["1.375", "Lett aktiv (1–3 ganger i uken)"],
                        ["1.55", "Moderat aktiv (3–5 ganger i uken)"],
                        ["1.725", "Veldig aktiv (6–7 ganger i uken)"]], "1.375")],
        "inputs": [("alder", "Alder", "35", "number"),
                   ("vekt", "Vekt (kg)", "80", "number"),
                   ("hoyde", "Høyde (cm)", "180", "number")],
        "js": """var konst = gs('kjonn')==='mann' ? 5 : -161;
var bmr = 10*g('vekt') + 6.25*g('hoyde') - 5*g('alder') + konst;
var f = parseFloat(gs('aktivitet')), tdee = bmr*f;
return {stor: fmtK(tdee), sub:'kcal per dag',
  celler:[['Hvileforbrenning',fmtK(bmr)+' kcal'],['Aktivitetsfaktor',gs('aktivitet')]],
  rader:[['Hvileforbrenning (BMR)',fmtK(bmr)+' kcal'],['Vedlikehold',fmtK(tdee)+' kcal'],
         ['Ned 0,5 kg/uke',fmtK(Math.max(tdee-500,1200))+' kcal'],['Opp 0,5 kg/uke',fmtK(tdee+500)+' kcal']]}""",
        "faq": [
            ["Hva er BMR?", "BMR (basal metabolic rate) er energien kroppen din forbrenner i full hvile. Det er størstedelen av det du forbrenner hver dag."],
            ["Hvor nøyaktig er kalkulatoren?", "Mifflin-St Jeor er den mest brukte formelen og treffer typisk innenfor ±10 % for de fleste. Individuelle variasjoner i muskelmasse og stoffskifte gir avvik."],
            ["Hvor mye skal jeg spise for å gå ned i vekt?", "Et vanlig og bærekraftig utgangspunkt er 500 kcal under vedlikeholdsbehov, som gir ca. 0,5 kg ned per uke. Ikke gå under 1 200 kcal uten legehjelp."]]},

    "prosentregner": {
        "navn": "Prosentregner", "icon": "％",
        "tittel": "Prosentregner – regn ut prosent raskt | Nettverktøy",
        "desc": "Gratis prosentregner: finn prosentandel, endring i prosent og prosent av et tall. Enkle prosentregninger på sekunder.",
        "intro": "Skriv inn to verdier og få alle vanlige prosentregninger med én gang.",
        "inputs": [("a", "Verdi A", "50", "number"), ("b", "Verdi B", "200", "number")],
        "js": """var a=g('a'), b=g('b');
var pAB = b!==0 ? a/b*100 : NaN, pBA = a!==0 ? b/a*100 : NaN;
var endr = a!==0 ? (b-a)/Math.abs(a)*100 : NaN;
return {stor: isFinite(pAB)? n1(pAB)+' %' : '–', sub:'A er av B',
  celler:[['B er av A', isFinite(pBA)? n1(pBA)+' %':'–'],['A % av B som tall', isFinite(pAB)? fmtK(a/100*b):'–']],
  rader:[['A er '+n1(pAB)+' % av B',''],['B er '+n1(pBA)+' % av A',''],['Endring A → B', isFinite(endr)? (endr>=0?'+':'')+n1(endr)+' %':''],['A % brukt på B', fmtK(a/100*b)] ]}""",
        "faq": [
            ["Hvordan regner jeg ut prosentøkning?", "(Ny verdi − gammel verdi) ÷ gammel verdi × 100. Skriver du inn gammel verdi som A og ny som B, viser kalkulatoren dette som «Endring A → B»."],
            ["Hvordan finner jeg X % av et tall?", "Multipliser tallet med prosenten delt på 100. Feltet «A % brukt på B» gjør akkurat dette."],
            ["Hva betyr prosentpoeng?", "Prosentpoeng er differansen mellom to prosenter. Fra 20 % til 25 % er det 5 prosentpoeng, men 25 % økning i relativ forstand."]]},

    "dato-kalkulator": {
        "navn": "Datokalkulator", "icon": "📅",
        "tittel": "Datokalkulator – dager mellom datoer | Nettverktøy",
        "desc": "Gratis datokalkulator: finn antall dager mellom to datoer, eller legg til/trekk fra dager på en dato. Raskt og enkelt.",
        "intro": "Antall dager mellom to datoer, pluss en ny dato når du legger til N dager.",
        "inputs": [("fra", "Startdato", "", "date"),
                   ("til", "Sluttdato", "", "date"),
                   ("n", "Legg til dager på startdato", "30", "number")],
        "js": """function p(d){ try{ return new Date(d+'T12:00:00'); }catch(e){ return null; } }
var f=p(gs('fra')), t=p(gs('til')), n=g('n');
if(!f || isNaN(f)){ return {stor:'Velg startdato', sub:'', celler:[], rader:[]}; }
var ny = new Date(f.getTime()+n*86400000);
var opts={day:'numeric',month:'short',year:'numeric'};
var df=f.toLocaleDateString('nb-NO',opts), dt=t&&!isNaN(t)?t.toLocaleDateString('nb-NO',opts):null, dn=ny.toLocaleDateString('nb-NO',opts);
var dager = (t&&!isNaN(t)) ? Math.round((p(gs('til'))-f)/86400000) : null;
return {stor: dager!==null ? n0(dager)+' dager' : dn, sub: dager!==null?'mellom datoene':'startdato + '+n0(n)+' dager',
  celler:[['Uker', dager!==null? n1(dager/7):'–'],['Startdato', df]],
  rader:[['Startdato',df],['Sluttdato',dt||'–'],['Dager mellom',dager!==null?n0(dager):'–'],['Startdato + '+n0(n)+' dager',dn]]}""",
        "faq": [
            ["Teller kalkulatoren med helger?", "Ja, alle dager telles med. Trenger du bare arbeidsdager, trekker du ca. 2/7 av dagene."],
            ["Kan jeg regne dager frem i tid?", "Ja – sett sluttdato fremover, eller bruk «legg til dager»-feltet for å få en ny dato direkte."],
            ["Stemmer det over tidssoner?", "Kalkulatoren bruker lokal dato ved middagstid for å unngå feil ved sommer-/vintertid."]]},

    "bmikalkulator": {
        "navn": "BMI-kalkulator", "icon": "⚖️",
        "tittel": "BMI-kalkulator – regn ut din Body Mass Index | Nettverktøy",
        "desc": "Gratis BMI-kalkulator: finn din Body Mass Index og hva tallet betyr, pluss normalvekt for din høyde.",
        "intro": "BMI = vekt delt på høyden i kvadrat. Skriv inn vekt og høyde, og se tallet og kategorien med én gang.",
        "inputs": [("vekt", "Vekt (kg)", "80", "number"), ("hoyde", "Høyde (cm)", "180", "number")],
        "js": """var v=g('vekt'), hm=g('hoyde')/100;
if(hm<=0){ return {stor:'–', sub:'', celler:[], rader:[]}; }
var bmi=v/(hm*hm), kat = bmi<18.5?'Undervektig':bmi<25?'Normalvekt':bmi<30?'Overvektig':'Fedme';
var lo=18.5*hm*hm, hi=24.9*hm*hm;
return {stor: n1(bmi), sub:kat,
  celler:[['Normalvekt for deg', n1(lo)+'–'+n1(hi)+' kg'],['Kategori',kat]],
  rader:[['Din BMI',n1(bmi)],['Kategori',kat],['Anbefalt intervall (BMI 18,5–24,9)',n1(lo)+'–'+n1(hi)+' kg']]}""",
        "faq": [
            ["Hva er normal-BMI?", "WHO opererer med 18,5–24,9 som normalområde. Under 18,5 er undervekt, 25–29,9 overvekt og 30+ fedme."],
            ["Er BMI nøyaktig for alle?", "Nei. BMI skiller ikke mellom muskler og fett, så svært muskuløse personer kan klassifiseres som overvektige. Det er et grovt mål for befolkning, ikke en diagnose."],
            ["Hva kan jeg bruke i stedet?", "Livvidde og midje-hofte-forhold sier mer om helserisiko. BMI er likevel et nyttig og gratis utgangspunkt."]]},
    "proteinbehov": {
        "navn": "Proteinbehov-kalkulator", "icon": "💪",
        "tittel": "Proteinbehov-kalkulator – hvor mye protein per dag? | Nettverktøy",
        "desc": "Gratis proteinbehov-kalkulator: finn hvor mange gram protein du trenger per dag basert på vekt, mål og livssituasjon.",
        "intro": "Anbefalt proteininntekt per kilo kroppsvekt varierer med målet ditt. Velg kategori og få gram per dag med én gang.",
        "selects": [("mal", "Ditt mål / situasjon", [
            ["1.2", "Vedlikehold (lite trening)"],
            ["1.6", "Generell trening"],
            ["1.8", "Muskelvekst / styrketrening"],
            ["2.0", "Ned i vekt (bevar muskler)"],
            ["1.5", "Eldre 65+ (forebygge muskeltap)"]], "1.6")],
        "inputs": [("vekt", "Vekt (kg)", "80", "number")],
        "js": """var f=parseFloat(gs('mal')), v=g('vekt'), d=v*f;
return {stor: n0(d)+' g', sub:'protein per dag',
  celler:[['Per kilo',n1(f)+' g/kg'],['Per måltid (4)',n0(d/4)+' g']],
  rader:[['Ditt behov',n0(d)+' g / dag'],['Fordelt på 4 måltider',n0(d/4)+' g per måltid'],['Til info: anbefalt minimum',n0(v*0.8)+' g (0,8 g/kg)']]}""",
        "faq": [
            ["Hvor mye protein trenger jeg?", "Anbefalt minimum er 0,8 g per kilo kroppsvekt. Trener du styrke ligger 1,6–1,8 g/kg optimalt, og på slankekur opptil 2,0 g/kg for å bevare muskelmassen."],
            ["Kan jeg få i meg for mye protein?", "For friske nyre­funksjoner er høyt inntak godt tolerert, men mer enn ca. 2,2 g/kg gir liten ekstra effekt. Nyresyke bør snakke med lege."],
            ["Beste kildene til protein?", "Fisk, kjøtt, egg, meieriprodukter, bønner og linser. En generell tommelfinger: 20–40 g protein per hovedmåltid dekker de fleste behov."]]},
}

TEMPLATE = """<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITTEL__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="https://arneshodzic.github.io/seo-verktoy/verktoy/__MAPPE__/">
<script type="application/ld+json">__SCHEMA_APP__</script>
<script type="application/ld+json">__SCHEMA_FAQ__</script>
<style>
:root{--bg:#0f172a;--card:#1e293b;--line:#334155;--txt:#e2e8f0;--mut:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--txt);line-height:1.6;padding:1rem}
.wrap{max-width:820px;margin:0 auto}
h1{font-size:1.6rem;margin:.5rem 0 1rem;color:#fff}
h2{font-size:1.15rem;margin:1.5rem 0 .5rem;color:#fff}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.25rem;margin-bottom:1rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.9rem}
label{display:block;font-size:.85rem;color:var(--mut);margin-bottom:.25rem}
input,select{width:100%;padding:.55rem .7rem;border-radius:8px;border:1px solid var(--line);background:#0b1220;color:var(--txt);font-size:1rem;color-scheme:dark}
input:focus,select:focus{outline:2px solid var(--acc)}
.res{background:linear-gradient(135deg,#0c4a6e,#075985);border-color:#0369a1;text-align:center;padding:1.5rem}
.res .big{font-size:2.2rem;font-weight:700;color:#fff;word-break:break-word}
.res .sub{color:#bae6fd;font-size:.95rem}
.row3{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.75rem;margin-top:1rem}
.cell{background:rgba(255,255,255,.08);border-radius:10px;padding:.7rem}
.cell b{display:block;font-size:1.15rem;color:#fff}
.cell span{font-size:.78rem;color:#bae6fd}
table{width:100%;border-collapse:collapse;font-size:.92rem}
td{padding:.45rem;border-bottom:1px solid var(--line)}
td:last-child{text-align:right;font-variant-numeric:tabular-nums;color:#fff}
.faq details{margin-bottom:.5rem}
.faq summary{cursor:pointer;font-weight:600;color:#fff;padding:.4rem 0}
a{color:var(--acc)}
footer{margin-top:2rem;color:var(--mut);font-size:.85rem;text-align:center}
</style>
</head>
<body>
<div class="wrap">
<h1>__ICON__ __NAVN__</h1>
<p style="color:var(--mut);margin-bottom:1rem">__INTRO__</p>

<div class="card res">
  <div class="big" id="stor">…</div>
  <div class="sub" id="sub"></div>
  <div class="row3" id="celler"></div>
</div>

<div class="card"><div class="grid" id="felt">__FELT__</div></div>
<div class="card"><table><tbody id="rader"></tbody></table></div>

<div class="card faq">
<h2>Ofte spurt</h2>
__FAQ__
</div>

<p style="margin-top:1rem"><a href="../../">&#8592; Alle verktøy</a></p>
<footer>Gratis · ingen reklame · ingen sporing · bygget automatisk __DATO__</footer>
</div>
<script>
function g(id){return parseFloat(document.getElementById(id).value)||0}
function gs(id){return document.getElementById(id).value}
function n0(x){return Math.round(x).toLocaleString('nb-NO')}
function n1(x){return (Math.round(x*10)/10).toLocaleString('nb-NO',{minimumFractionDigits:1,maximumFractionDigits:1})}
function fmtK(x){return n0(x)+' kr'}
function beregn(){var r=(function(){
__JS__
})();if(!r)return;r.stor&&(document.getElementById('stor').textContent=r.stor);r.sub!=null&&(document.getElementById('sub').textContent=r.sub);
var c=document.getElementById('celler');c.innerHTML='';(r.celler||[]).forEach(function(x){var d=document.createElement('div');d.className='cell';d.innerHTML='<span>'+x[0]+'</span><b>'+x[1]+'</b>';c.appendChild(d)});
var tb=document.getElementById('rader');tb.innerHTML='';(r.rader||[]).forEach(function(x){var tr=document.createElement('tr');tr.innerHTML='<td>'+x[0]+'</td><td>'+(x[1]||'')+'</td>';tb.appendChild(tr)})}
document.querySelectorAll('#felt input,#felt select').forEach(function(i){i.addEventListener('input',beregn);i.addEventListener('change',beregn)});
beregn();
</script>
</body>
</html>
"""

def render(key, dato=None):
    spec = LIB[key]
    dato = dato or datetime.date.today().isoformat()
    url = f"https://arneshodzic.github.io/seo-verktoy/verktoy/{key}/"
    app_schema = json.dumps({"@context": "https://schema.org", "@type": "WebApplication",
                             "name": spec["navn"], "url": url,
                             "applicationCategory": "UtilitiesApplication",
                             "operatingSystem": "Nettleser",
                             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NOK"},
                             "inLanguage": "nb-NO"}, ensure_ascii=False)
    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                             "mainEntity": [{"@type": "Question", "name": q,
                                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                                            for q, a in spec["faq"]]}, ensure_ascii=False)
    felt = ""
    for sid, label, opts_list, default in spec.get("selects", []):
        opts = "".join(f'<option value="{v}"{" selected" if v == default else ""}>{_esc(t)}</option>'
                       for v, t in opts_list)
        felt += f'<div><label>{_esc(label)}</label><select id="{sid}">{opts}</select></div>\n'
    for iid, label, default, typ in spec.get("inputs", []):
        extra = f'value="{default}"'
        felt += f'<div><label>{_esc(label)}</label><input type="{typ}" id="{iid}" {extra}></div>\n'
    faq_html = "\n".join(f'<details{" open" if i == 0 else ""}><summary>{_esc(q)}</summary>{_esc(a)}</details>'
                         for i, (q, a) in enumerate(spec["faq"]))
    html = (TEMPLATE
            .replace("__TITTEL__", _esc(spec["tittel"]))
            .replace("__DESC__", _esc(spec["desc"]))
            .replace("__MAPPE__", key)
            .replace("__ICON__", spec["icon"])
            .replace("__NAVN__", _esc(spec["navn"]))
            .replace("__INTRO__", _esc(spec["intro"]))
            .replace("__SCHEMA_APP__", app_schema)
            .replace("__SCHEMA_FAQ__", faq_schema)
            .replace("__FELT__", felt)
            .replace("__FAQ__", faq_html)
            .replace("__DATO__", dato)
            .replace("__JS__", spec["js"]))
    return html

def publiser():
    ko_path = os.path.join(ROOT, "ko.txt")
    with open(ko_path, encoding="utf-8") as f:
        lines = f.readlines()
    idx = next((i for i, l in enumerate(lines) if l.strip() and not l.startswith("#")), None)
    if idx is None:
        print("KO_TOM")
        return 1
    key = lines[idx].split("|")[0].strip()
    if key not in LIB:
        print(f"IKKE_I_BIBLIOTEK:{key}")
        return 1
    navn = lines[idx].split("|")[1].strip() if "|" in lines[idx] else LIB[key]["navn"]
    dato = datetime.date.today().isoformat()
    d = os.path.join(ROOT, "verktoy", key)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(render(key, dato))
    lines.pop(idx)
    with open(ko_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    with open(os.path.join(ROOT, "logg.txt"), "a", encoding="utf-8") as f:
        f.write(f"{dato}|{navn}|publisert|https://arneshodzic.github.io/seo-verktoy/verktoy/{key}/\n")
    print(f"PUBLISERT:{navn}|{key}|igjen_i_ko={sum(1 for l in lines if l.strip() and not l.startswith('#'))}")
    return 0

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--test":
        os.makedirs(TMP, exist_ok=True)
        k = args[1]
        path = os.path.join(TMP, k + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(k))
        print("TEST_OK:" + path)
    elif args and args[0] == "--alle-test":
        os.makedirs(TMP, exist_ok=True)
        for k in LIB:
            p = os.path.join(TMP, k + ".html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(render(k))
        print(f"TEST_OK:{len(LIB)} filer i tmp/")
    elif args and args[0] == "--publiser":
        sys.exit(publiser())
    else:
        print(__doc__)
