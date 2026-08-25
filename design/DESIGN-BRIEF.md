# DESIGN-BRIEF: Smartkalkulator.no (ny identitet)

## Bakgrunn
Vi har en fungerende samling norske kalkulatorer som i dag kjører på
https://arneshodzic.github.io/seo-verktoy/ (repo: seo-verktoy). Funksjonaliteten er ferdig
og testet — men designet er generisk og kjedelig. Vi relanserer som
**smartkalkulator.no** og trenger en moderne, edgy, premium identitet.

## Hva produktet ER
- 12+ selvstendige kalkulatorer (moms, lån, feriepenger, kalorier, BMI, elbillading osv.)
- Norsk målgruppe, norsk tekst (bokmål)
- Målgruppen: vanlige folk som raskt vil regne ut noe — men siden skal FELE som et
  moderne fintech-merke, ikke et støvet verktøysted fra 2010
- Alt er statisk HTML med vanilla JS — ingen rammeverk, ingen byggesteg
- MERKEVARE: alle verktøy heter «X-kalkulator/-beregner». Nye verktøy kommer
  kontinuerlig, alltid i samme format.

## Logo / merkevare
Konsept: **en kalkulator som er SMART — kul og edgy, ikke søt**.
Mørk, matt kalkulator-karakter/symbol med glødende skjerm, skarpe kanter, attitude.
Neon-cyan aksent på dyp marineblå. Se utkast: `logo-utkast.png` (AI-konseptskisse —
vi ønsker denne retningen, men renere/vektormessig). Lever logo som ren SVG
(merke alene + merke med wordmark «Smartkalkulator»).

Navnet er **Smartkalkulator** (ett ord, stor S). Ordet «Nettverktøy» skal ikke
finnes noe sted.

## STRUKTUR: kategorifaner på forsiden (VIKTIG)
Forsiden skal IKKE være én lang flat liste. Den skal ha **kategorifaner** (tabs):
  💰 Finans · 🚗 Bil & reise · 💪 Livsstil & helse · 📅 Hverdag (+ 🔧 Annet ved behov)
Én kategori aktiv om gangen, klikk bytter panel. Mobilvennlig (wrap til rader).
Hver kalkulator tilhører nøyaktig én kategori via `kat`-feltet i LIB-dicten i
generer.py («finans»/«bil»/«livsstil»/«hverdag»/«annet»). build.py bygger allerede
faner mekanisk — behold mekanismen, restyle den. Se ny `eksempel-hub.html`.

## Visuell retning (veiledende, overstyr gjerne)
- Mørkt tema (#0f172a/#1e293b nå) men MED PERSONLIGHET: gradienter, dybde,
  glassmorfisme el.l. — gjør det levende
- Aksent: elektrisk cyan/blå (#38bdf8-området) + gjerne én sekundærfarge
- Typografi: Inter/Manrope/Sora-lignende, tydelig hierarki; store resultattall
  skal se PREMIUM ut
- Mikroanimasjoner: tell-opp av resultater, subtile hover/focus-effekter
- Layout: luftige kort; perfekt på 360px bredde og opp (mest trafikk er mobil)

## Tekniske krav (VIKTIG)
1. Statisk HTML/CSS/vanilla JS — ingen npm/build-steg (Google Fonts-lenke OK)
2. Sider genereres av generer.py fra TEMPLATE-variabelen. Lever designet som
   **én mal-fil** med plassholdere:
   `__TITTEL__ __DESC__ __MAPPE__ __ICON__ __NAVN__ __INTRO__ __SCHEMA_APP__ __SCHEMA_FAQ__ __FELT__ __FAQ__ __DATO__ __JS__`
   der `__FELT__` = input/select-felter, `__JS__` = logikk som returnerer
   `{stor, sub, celler:[[label,verdi]], rader:[[label,verdi]]}`, `__FAQ__` = FAQ-details
3. Behold SEO-strukturen: title, meta description, canonical, schema.org
   WebApplication + FAQPage JSON-LD, FAQ-seksjon, «Alle kalkulatorer»-lenke
4. Restyle også hub-malen i build.py (kategori-fanene over)
5. Tilgjengelighet: kontrast, synlige focus-states, labels på alle felt

## Leveranse fra deg (Claude)
1. Ny TEMPLATE (komplett index.html-mal med plassholdere over)
2. Oppdatert hub-del i build.py (samme mekanisme, nytt uttrykk)
3. Logo som SVG (merke + wordmark)
4. Kort endringslogg

## Filstruktur i repoet
```
generer.py                       <- TEMPLATE (malen du erstatter) + LIB (12 kalkulatorer m/kat)
build.py                         <- bygger hub/index.html med kategorifaner
verktoy/<navn>/index.html        <- ferdige sider
design/logo-utkast.png           <- AI-konseptskisse av logo
design/eksempel-hub.html         <- nåværende hub med faner (restyle-mål)
design/pakke-til-claude/eksempel-navaerende-design.html <- eksempelside slik den ser ut nå
```
