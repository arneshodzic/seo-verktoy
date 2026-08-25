# DESIGN-BRIEF: Smartkalkulator.no (ny identitet)

## Bakgrunn
Vi har en fungerende samling norske nettverktøy/kalkulatorer som i dag kjører på
https://arneshodzic.github.io/seo-verktoy/ (repo: seo-verktoy). Funksjonaliteten er ferdig
og testet — men designet er grådig generisk og kjedelig. Vi skal relansere som
**smartkalkulator.no** og trenger en moderne, edgy, premium identitet.

## Hva produktet ER
- 12+ selvstendige kalkulator-verktøy (moms, lån, feriepenger, kalorier, BMI, elbillading osv.)
- Norsk målgruppe, norsk tekst (bokmål)
- Målgruppen: vanlige folk som raskt vil regne ut noe — men siden skal FELE som et
  moderne fintech-merke, ikke et støvet verktøy-hjemmeside fra 2010
- Alle sider er statisk HTML med vanilla JS — ingen rammeverk, ingen build-steg nødvendig

## Logo / merkevare
Konsept: **en kalkulator som er SMART — kul og edgy, ikke søt**.
Tenk: mørk, matt kalkulator-karakter/symbol med glødende skjerm, skarpe kanter,
litt "attitude". Neon-cyan aksent på dyp marineblå bakgrunn. Se utkast:
`design/logo-utkast.png` (AI-generert konseptskisse — vi ønsker noe i denne retningen,
men renere/mere vektormessig). Lever gjerne forslag som ren SVG.

Navnet er **Smartkalkulator** (ett ord, stor S). Ikke bruk "Nettverktøy" noe sted.

## Visuell retning (veiledende, overstyr gjerne)
- Mørkt tema (nå: #0f172a bakgrunn, #1e293b kort) men MED MER PERSONLIGHET:
  gradienter, dybde, glassmorfisme eller lignende — gjør det levende
- Aksentfarge: elektrisk cyan/blå (#38bdf8-området) — gjerne med én sekundær
- Typografi: moderne (Inter/Manrope/Sora-lignende), tydelig hierarki,
  store tall i resultatområdet skal se PREMIUM ut
- Mikroanimasjoner: resultater som teller opp, subtile hover-effekter, smooth focus
- Layout: luftige kort, god mobil-opplevelse (mesteparten av trafikken er mobil)

## Tekniske krav (VIKTIG)
1. Alt forblir **statisk HTML/CSS/vanilla JS** — ingen npm, ingen CDN-avhengigheter
   som krever byggesteg (Google Fonts-lenke er OK)
2. Siden genereres av `generer.py` fra en HTML-mal (TEMPLATE-variabelen) — så
   lever designet som **én mal-fil** med plassholdere:
   `__TITTEL__ __DESC__ __MAPPE__ __ICON__ __NAVN__ __INTRO__ __SCHEMA_APP__ __SCHEMA_FAQ__ __FELT__ __FAQ__ __DATO__ __JS__`
   ...der `__FELT__` er input/select-felter, `__JS__` er kalkyle-logikken som returnerer
   `{stor, sub, celler:[[label,verdi]], rader:[[label,verdi]]}`, og `__FAQ__` er FAQ-details.
3. Behold SEO-strukturen: title, meta description, canonical, schema.org
   WebApplication + FAQPage JSON-LD, FAQ-seksjon, «Alle verktøy»-lenke
4. Hub-siden (index.html) lister alle verktøy som klikkbare kort — design den også
5. Responsiv: perfekt på 360px bredde og opp
6. Tilgjengelighet: kontrast, focus-states, labels på alle felt

## Leveranse
1. Ny TEMPLATE (komplett index.html-mal med plassholderne over)
2. Ny hub-mal
3. CSS samlet i malen (eller egen style.css — si ifra)
4. Logo som SVG (merke + evt. wordmark)
5. Kort liste over hva som endret seg

## Filstruktur i repoet
```
generer.py          <- inneholder TEMPLATE (malen du erstatter) + LIB (12 verktoy)
build.py            <- bygger hub/index.html
verktoy/<navn>/     <- ferdige sider
design/logo-utkast.png  <- AI-konseptskisse av logo
```
