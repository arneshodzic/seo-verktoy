# Smartkalkulator – oppdatert designpakke

Innhold:

```
generer.py            <- ny TEMPLATE + LIB (kopier over repo-roten i seo-verktoy)
build.py              <- ny hub-del med kategorifaner (kopier over repo-roten)
design/
  mal-verktoyside.html   frittstaende kopi av malen med alle plassholdere
  ENDRINGSLOGG.md        hva som er endret og hvorfor
  DESIGN-BRIEF.md        briefen leveransen er laget mot
  logo/
    smartkalkulator-logo.svg        merke + wordmark
    smartkalkulator-merke.svg       merke alene, med glod
    smartkalkulator-merke-flat.svg  flat variant (favicon, lyse flater)
forhandsvis/
  index.html            ferdig bygget hub - apne denne i nettleser
  verktoy/*/index.html  alle 12 kalkulatorsider, ferdig rendret
```

## Ta i bruk
1. Kopier `generer.py` og `build.py` over de gamle i repoet `seo-verktoy`.
2. `python generer.py --alle-test` for a rendre alt til `tmp/` uten a rore ko/logg.
3. `python generer.py --publiser` som for, deretter `python build.py`.
4. Legg logo-SVG-ene i `design/logo/` i repoet.

## Merk
- `logo-utkast.png` er ikke tatt med (ligger allerede i repoet under `design/`).
- Canonical-URL-ene peker fortsatt pa `arneshodzic.github.io/seo-verktoy/`.
  Ved bytte til smartkalkulator.no: sok og erstatt den strengen i `generer.py`
  (TEMPLATE + `render()`) og i `build.py` (`BASE`).
- `forhandsvis/` er kun til visning; den skal ikke inn i repoet.
