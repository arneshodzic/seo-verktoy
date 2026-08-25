# Endringslogg – Smartkalkulator ny identitet

Dato: 2026-08-25

## 1. Ny TEMPLATE i `generer.py`
Hele `TEMPLATE`-variabelen er byttet ut (nå `r"""…"""` fordi JS-en inneholder regex).
Samme mal ligger også som frittstående fil: `mal-verktoyside.html`.

**Alle 12 plassholdere beholdt og verifisert:** `__TITTEL__ __DESC__ __MAPPE__ __ICON__
__NAVN__ __INTRO__ __SCHEMA_APP__ __SCHEMA_FAQ__ __FELT__ __FAQ__ __DATO__ __JS__`.
`__JS__`-kontrakten er uendret: snippeten returnerer fortsatt
`{stor, sub, celler:[[label,verdi]], rader:[[label,verdi]]}`, og hjelpefunksjonene
`g gs n0 n1 fmtK` finnes med samme signatur.

Design:
- **Mørkt premium-tema med dybde:** to radiale auraer (cyan + indigo) og et svakt rutenett
  som fader ut mot toppen, faste bak innholdet. Kort med gradient, hairline-kant og myk dybdeskygge.
- **Aksent:** elektrisk cyan `#22d3ee` (+ `#67e8f9`), sekundær indigo `#818cf8`.
- **Typografi:** Sora 600/700 til display/tall + Inter 400/500/600 til brødtekst (én Google Fonts-lenke,
  `display=swap`). Alle tall bruker `tabular-nums`.
- **Resultatkortet** er hovedgrepet: eyebrow «RESULTAT», resultattall i `clamp(2.3rem…3.4rem)` med
  gradient-fyll og cyan glød, lysende hairline i topp og radial glow.
- **Mikroanimasjoner:** tell-opp av resultattallet og av nøkkeltall-cellene (~460 ms, easeOutCubic),
  glød-puls når verdien endres, stagger-innfading av celler og detaljrader, løft/glow på hover.
  Tell-opp-funksjonen finner første tall i strengen og beholder tekst rundt, så `«3 211 kr / mnd»`,
  `«5,3 %»`, `«1,6 g/kg»` og `«59,9–80,7 kg»` formateres riktig med nb-NO-gruppering.
- **Mobil først:** ett kort per rad, resultat øverst (`order:-1`), 48 px+ touch-mål. Fra 880 px
  splittes det i to kolonner (felt til venstre, sticky resultat til høyre) og
  detaljer/FAQ/CTA legger seg i en rolig lesekolonne på 800 px. Verifisert uten
  horisontal overflow på 360 px.
- **Egen kalkulator-knapp/faneuttrykk:** custom cyan chevron i `<select>`, cyan fokusring
  + glow på alle felt, FAQ med roterende chevron og aktiv cyan kant.
- **Struktur lagt til:** topplinje med logo + «Alle kalkulatorer», tillitsmarkører
  (Gratis / Ingen registrering / Ingen sporing / Oppdatert `__DATO__`), «Dine tall»- og
  «Detaljer»-kort, CTA-kort mot forsiden, ny bunn.

SEO/tilgjengelighet:
- Beholdt: `<title>`, meta description, canonical, `WebApplication`- og `FAQPage`-JSON-LD,
  FAQ-seksjon og «Alle kalkulatorer»-lenke. Validert som gyldig JSON på alle 12 sidene.
- Lagt til: `theme-color`, Open Graph (`og:title/description/url/site_name/locale/type`),
  SVG-favicon som data-URI (ingen ekstra filavhengighet).
- `prefers-reduced-motion: reduce` slår av all animasjon (tell-opp settes direkte).
- Skjult `role="status" aria-live="polite"` som annonserer sluttresultatet (debounced 700 ms),
  så skjermleser ikke leser hver animasjonsramme.
- `<noscript>`-varsel i feltkortet.
- Kontrast målt på alle tekstpar: laveste er 6,6:1, resten 9–20:1. Cyan CTA-knapp: 9,3:1.

Små endringer i `render()` (begrunnet av krav 5 i briefen):
- `<label for="…">` + `name` på alle felt (labels var tidligere ikke koblet til inputene).
- `inputmode="decimal"` på nummerfelt → numerisk tastatur på mobil.

Merkevare:
- «Nettverktøy» er fjernet fra alle 12 titler i `LIB` → `| Smartkalkulator`.
  Ordet finnes ikke lenger i noen generert fil.

## 2. Hub-delen i `build.py`
Mekanismen er beholdt: `KATEGORIER`, gruppering på `kat` fra `LIB`, `KAT_EKSTRA`,
`__ANTALL__/__FANER__/__PANELS__`-erstatning, samme klassenavn (`.faner .fane .panel .t .i .n .d`).

- **Faner:** pille-faner med antall-badge per kategori; aktiv fane er cyan gradient-pille.
  Bytter nå via klasse (`.aktiv`) og `hidden`-attributt i stedet for inline-stiler.
- **Tilgjengelig faneliste:** `role="tablist"/"tab"/"tabpanel"`, `aria-selected`,
  `aria-controls`, roving `tabindex`, og piltast/Home/End-navigasjon.
- **Verktøykort:** 1 kolonne på mobil, 2 fra 660 px. Ikon i cyan-tile, navn i Sora,
  beskrivelse klippet til 3 linjer, løft + cyan glow og radial highlight på hover/fokus.
- **Hero:** inline SVG-merke + wordmark, «Regn ut svaret på sekunder», teller for antall kalkulatorer.
- **SEO lagt til:** canonical, Open Graph, favicon og `CollectionPage` + `ItemList`-JSON-LD
  generert automatisk fra verktøylisten.

To feilrettinger i `extract()` (påvirket hubben direkte):
- Navn ble kuttet på bindestrek: `«BMI-kalkulator»` ble «BMI» og
  `«Rentes rente-kalkulator»` ble «Rentes rente». Nå brukes `navn` fra `LIB`, med
  splitt bare på separator med mellomrom rundt som fallback.
- Ikon-fallback for håndlagde verktøy plukket hele `<h1>`-teksten
  («🚗 Bilkostnadskalkulator»). Nå strippes markup og bare første symbol brukes.

## 3. Logo (`logo/`)
Rensket vektorversjon av utkastet: matt, mørkt kalkulatorhus med kuttet hjørne (skarp kant),
glødende cyan kontur, lysende skjerm med lyn-glyf, tastatur med én cyan aksenttast, og gnisten
fra skissen i topp høyre.

- `smartkalkulator-merke.svg` – merket alene, med glød (gradienter + `feGaussianBlur`). 96×96.
- `smartkalkulator-logo.svg` – merke + wordmark «Smart**kalkulator**» og linjen
  «RASKE SVAR · GRATIS». 420×96.
- `smartkalkulator-merke-flat.svg` – flat variant uten filtre for favicon/små flater
  og for bruk på lys eller cyan bakgrunn.
- Samme merke ligger inline (uten filtre) i topplinjen på verktøysidene og i hubben,
  samt som komprimert data-URI-favicon.

Merk: wordmarken bruker `<text>` med `font-family="Sora, Manrope, Inter, …"`. Til web er det
riktig (Sora lastes allerede); til trykk/logo-arkiv bør teksten konverteres til outlines.

## 4. Rettet enhetsfeil i LIB (kroner der det ikke er kroner)
`fmtK()` legger på « kr». To kalkulatorer brukte den på verdier som ikke er penger:

- **kaloriberegner:** viste `2 413 kr` og `1 755 kr kcal`. Nå `n0()`:
  stort tall `2 413` med undertekst «kcal per dag», celler/rader `1 755 kcal`,
  `2 413 kcal`, `1 913 kcal`, `2 913 kcal`.
- **prosentregner:** «A % av B som tall» viste `100 kr` for to generelle tall.
  Nå en lokal `tall()`-hjelper som viser heltall rent og ellers én desimal:
  50 av 200 → `100`, 12,5 av 33 → `4,1`.

Gjennomgått resten: `proteinbehov`, `bmikalkulator` og `enhetskonverterer` bruker
ikke `fmtK` i det hele tatt (bruker `n0`/`n1` + egen enhet), og er korrekte.
Gjenstående `fmtK`-bruk er kun i kalkulatorer som faktisk regner kroner:
moms, lån, feriepenger, rentes rente og elbil-ladekostnad.

## Verifisert
- `python generer.py --alle-test` → 12/12 sider, ingen ubyttede plassholdere.
- `python build.py` → 13 verktøy i 4 kategorier, riktige navn og ikoner.
- Alle 12 sider + hub: gyldig JSON-LD, title/description/canonical på plass, 0 treff på «Nettverktøy».
- Tell-opp verifisert i nettleser med ekte malkode (`4 178 → 7 669 → … → 12 500 kr`).
- Faner: klikk, piltaster, Home/End, `aria-selected` og panelbytte verifisert.
- 360 px: ingen horisontal overflow, touch-mål 51 px.
