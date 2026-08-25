# -*- coding: utf-8 -*-
"""Kjorer hver verktuys JS-logikk i Node mot standardinndata og sjekker tallene."""
import sys, subprocess, json, math
sys.path.insert(0, ".")
from generer import LIB

HEADER = """const IN=__IN__;
function g(id){return parseFloat(IN[id])||0}
function gs(id){return String(IN[id])}
function n0(x){return Math.round(x).toLocaleString('nb-NO')}
function n1(x){return (Math.round(x*10)/10).toLocaleString('nb-NO',{minimumFractionDigits:1,maximumFractionDigits:1})}
function fmtK(x){return n0(x)+' kr'}
(async()=>{ const r = (function(){ __BODY__ })(); return r; })().then(r=>console.log('RES:'+JSON.stringify(r))).catch(e=>{console.error(e);process.exit(1)})
"""

DEFAULTS = {
    "moms-kalkulator": {"retning": "leggtil", "belop": "10000", "sats": "25"},
    "laanekalkulator": {"belop": "300000", "rente": "5.2", "aar": "10"},
    "feriepenger": {"sats": "10.2", "lonn": "600000"},
    "rentes-rente": {"start": "100000", "mnd": "1000", "rente": "5", "aar": "10"},
    "elbil-ladekostnad": {"forbruk": "18", "pris": "1.5", "km": "15000",
                          "bforbruk": "6.5", "bpris": "21"},
    "kaloriberegner": {"kjonn": "mann", "aktivitet": "1.375", "alder": "35", "vekt": "80", "hoyde": "180"},
    "proteinbehov": {"mal": "1.6", "vekt": "80"},
    "bmikalkulator": {"vekt": "80", "hoyde": "180"},
    "prosentregner": {"a": "50", "b": "200"},
    "dato-kalkulator": {"fra": "2026-08-01", "til": "2026-09-01", "n": "30"},
    "enhetskonverterer": {"fra": "km", "til": "mil", "verdi": "5"},
    "alder": {"fdato": "1990-01-01"},
}

def to_num(s):
    if s is None:
        return None
    neg = s.strip().startswith("-")
    digits = s.replace("\u00a0", "").replace("\u202f", "").replace(",", ".").replace(" ", "")
    digits = "".join(c for c in digits if c.isdigit() or c == "." or c == "-")
    return float(digits) if digits else None

def rows_text(res):
    return " ".join(str(v) for row in res["rader"] for v in row)

ok = 0
for key, spec in LIB.items():
    script = HEADER.replace("__IN__", json.dumps(DEFAULTS[key])).replace("__BODY__", spec["js"])
    p = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    if p.returncode != 0:
        print(f"FEIL {key}: {p.stderr[:400]}"); continue
    res = json.loads(p.stdout.strip().split("RES:", 1)[1])
    try:
        if key == "moms-kalkulator":
            assert to_num(res["stor"]) == 2500 and "12 500" in rows_text(res).replace("\u00a0", " ")
        elif key == "laanekalkulator":
            b, r, n = 300000, 0.052 / 12, 120
            t = b * r / (1 - (1 + r) ** -n)
            assert abs(to_num(res["stor"]) - t) < 2, (res["stor"], t)
            assert abs(to_num(res["rader"][2][1]) - (t * n - b)) < 5
        elif key == "feriepenger":
            assert to_num(res["stor"]) == 61200, res["stor"]
        elif key == "rentes-rente":
            r_, n_ = 0.05 / 12, 120
            fv = 100000 * (1 + r_) ** n_ + 1000 * (((1 + r_) ** n_ - 1) / r_)
            assert abs(to_num(res["stor"]) - fv) < 50, (res["stor"], fv)
        elif key == "elbil-ladekostnad":
            assert to_num(res["stor"]) == 4050, res["stor"]
            assert "16 425" in rows_text(res).replace("\u00a0", " "), rows_text(res)
        elif key == "kaloriberegner":
            bmr = 10 * 80 + 6.25 * 180 - 5 * 35 + 5
            assert abs(to_num(res["stor"]) - bmr * 1.375) < 2, res["stor"]
        elif key == "proteinbehov":
            assert to_num(res["stor"]) == 128 and res["sub"].startswith("protein")
            assert "0,8 g/kg" in rows_text(res), rows_text(res)
        elif key == "bmikalkulator":
            assert to_num(res["stor"]) == 24.7 and res["sub"] == "Normalvekt", res
        elif key == "prosentregner":
            assert res["stor"].startswith("25") and "+300" in rows_text(res), res["stor"]
        elif key == "dato-kalkulator":
            assert to_num(res["stor"]) == 31 and "31. aug" in rows_text(res), res
        elif key == "enhetskonverterer":
            assert res["stor"].startswith("0,5 mil"), res["stor"]
        elif key == "alder":
            assert res["stor"] == "36 \u00e5r" or res["stor"].startswith("36"), res["stor"]
            assert res["sub"].startswith("og "), res
        print(f"OK   {key}: stor='{res['stor']}'")
        ok += 1
    except AssertionError as e:
        print(f"TALLFEIL {key}: {e}")
print(f"\n{ok}/{len(LIB)} verktoy regner korrekt")
sys.exit(0 if ok == len(LIB) else 1)
