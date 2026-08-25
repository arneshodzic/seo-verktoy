# -*- coding: utf-8 -*-
"""Felles footer + juridiske drilldown-sider for Fristkalender og Smartkalkulator.
Bruk: from footer import footer_html, juridisk_side, FOOTER_CSS
footer_html(side, lenker) -> HTML-streng (sett inn i <footer>-taggen)
juridisk_side(tittel, innhold_html) -> fullside HTML
"""
import datetime, os

AAR = datetime.date.today().year

FOOTER_CSS = """
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
"""

def footer_html(navn, lenker, juridisk_base="."):
    """navn: 'Fristkalender'/'Smartkalkulator'. lenker: liste med (tittel,url).
    juridisk_base: relativ sti til juridisk-mappen ('../juridisk' fra under-sider)."""
    kat = []
    pop = []
    jur = [
        ("Personvern", f"{juridisk_base}/personvern/"),
        ("Vilkår", f"{juridisk_base}/vilkar/"),
        ("Cookies", f"{juridisk_base}/cookies/"),
        ("Om oss", f"{juridisk_base}/om-oss/"),
    ]
    # del lenker i kategori/populær
    for t, u in lenker:
        if len(kat) < 6:
            kat.append((t, u))
        else:
            pop.append((t, u))
    def lst(items):
        return "\n".join(f'<a href="{u}">{t}</a>' for t, u in items)
    if navn == "Fristkalender":
        soster = '<a href="../">Smartkalkulator.no</a>'
    else:
        soster = '<a href="../fristkalender/">Fristkalender.no</a>'
    return f'''
<div class="site-footer">
  <div class="foot-grid">
    <div class="brand-col">
      <div class="logo">{navn}</div>
      <p>Gratis, oppdatert hver dag. Aldri glipp en frist eller et regnestykke igjen.</p>
    </div>
    <div class="foot-col">
      <div class="foot-h">Utforsk</div>
      {lst(kat)}
    </div>
    <div class="foot-col">
      <div class="foot-h">Populært</div>
      {lst(pop)}
    </div>
    <div class="foot-col">
      <div class="foot-h">Juridisk</div>
      {lst(jur)}
    </div>
  </div>
  <div class="foot-bot">
    © {AAR} {navn} &middot; en gratis tjeneste i samme familie som {soster}<br>
    Opplysningene er veiledende – sjekk alltid hos offentlig kilde ved tvil.
  </div>
</div>'''

DOCSIDER = {
    "personvern": ("Personvern", """
<p>Vi respekterer ditt personvern. Denne siden er bygget for å være enkel og trygg:</p>
<h3>Ingen sporing</h3>
<p>Vi bruker ingen tredjeparts analyseverktøy, ingen informasjonskapsler til markedsføring,
og ingen profilering. Vi lagrer ingenting du skriver inn – alle beregninger skjer i nettleseren din.</p>
<h3>Ingen kontohåndtering</h3>
<p>Det finnes ingen pålogging, ingen abonnement og ingen registrering. Vi vet ikke hvem du er.</p>
<h3>Eksterne lenker</h3>
<p>Siden lenker til offentlige kilder (Skatteetaten, Vegvesen, NAV, Forbrukerrådet). Når du klikker
videre dit, gjelder deres personvernerklæring.</p>
<h3>Kontakt</h3>
<p>Spørsmål om personvern? Send oss en melding via <a href="om-oss/">kontaktsiden</a>.</p>
"""),
    "vilkar": ("Vilkår", """
<h3>Ingen garanti</h3>
<p>Innholdet leveres slik det er ("as-is") uten garantier. Beregninger og frister er ment som
veiledning, ikke profesjonell rådgivning. For skatt, rettigheter og lover gjelder alltid
offentlig kilde og gjeldende regelverk.</p>
<h3>Ansvarsfraskrivelse</h3>
<p>Vi er ikke ansvarlige for konsekvenser av å stole på informasjonen her. Sjekk alltid selv
hos myndighet eller rådgiver før du tar beslutninger som har økonomiske eller juridiske virkninger.</p>
<h3>Endringer</h3>
<p>Vilkårene kan endres. Den gjeldende versjonen ligger alltid her.</p>
"""),
    "cookies": ("Cookies", """
<p>Denne siden bruker så lite som mulig av informasjonskapsler:</p>
<h3>Nødvendige</h3>
<p>Vi lagrer ingen sesjons-data lokalt som kan kobles til deg. Eventuelle favoritt-valg lagres
kun i din egen nettleser (localStorage) og deles ikke med oss.</p>
<h3>Tredjepart</h3>
<p>Ingen annonse- eller analyse-nettverk får data fra deg via denne siden.</p>
<h3>Dine valg</h3>
<p>Du kan når som helst slette informasjonskapsler i nettleseren din. Det påvirker ikke
funksjonaliteten vår.</p>
"""),
    "om-oss": ("Om oss", """
<p>Vi bygger gratis norske verktøy som gjør hverdagen enklere – kalkulatorer og fristoversikter
som holdes oppdatert automatisk, hver dag.</p>
<h3>Hvorfor</h3>
<p>Fordi viktige frister og regnestykker ikke skal koste noe, og ikke skal ligge spredt over
ti ulike tunge offentlige sider.</p>
<h3>Hvordan vi finansieres</h3>
<p>Siden kan vise annonseplasser fra uavhengige nettverk. Det påvirker ikke innholdet vårt –
vi rangerer verktøy etter nytte, ikke etter betaling.</p>
<h3>Kontakt</h3>
<p>Tips, feil eller ønsker? Send en melding. Vi leser alt.</p>
"""),
}

def juridisk_side(slug, juridisk_base=".."):
    tittel, innhold = DOCSIDER[slug]
    return f'''<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{tittel} – Fristkalender</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{juridisk_base}/assets/style.css">
</head>
<body>
<div class="wrap" style="max-width:760px">
<header style="text-align:left;padding:2rem 0 1rem">
  <a class="logo" href="{juridisk_base}/">Frist<i>kalender</i></a>
  <h1 class="slag" style="text-align:left;margin-top:.8rem">{tittel}</h1>
</header>
<main style="color:var(--mut);line-height:1.7;font-size:1rem">
{innhold}
</main>
{footer_html("Fristkalender", [("Alle frister","{juridisk_base}/")], juridisk_base="{juridisk_base}/juridisk")}
</div>
</body></html>'''
