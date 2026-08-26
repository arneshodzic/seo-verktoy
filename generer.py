# -*- coding: utf-8 -*-
"""Verktøyfabrikk: genererer verktøysider fra innebygd bibliotek.
Bruk:
  python generer.py --test <nokkel>   # rendrer til tmp/ uten å røre kø/logg
  python generer.py --alle-test       # rendrer alle til tmp/
  python generer.py --publiser        # tar første ledige fra ko.txt, bygger, stryker, logger
"""
import os, sys, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(ROOT, "tmp")

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

LIB = {
    # ------------------------------------------------------------- økonomi
    "moms-kalkulator": {
        "kat": "finans",
        "navn": "Momskalkulator", "icon": "🧾",
        "tittel": "Momskalkulator – legg til eller fjern 25 % mva | Smartkalkulator",
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
            ["Hvor mye er moms i Norge?", "Alminnelig momssats er 25 %. Mat og drikke har 15 %, og noen tjenester som persontransport og kinobilletter har 12 %."],
            ["Hvordan regner jeg moms baklengs?", "Del bruttobeløpet på 1,25 (ved 25 % sats). Da får du beløpet uten moms. Momsen er differansen. Kalkulatoren gjør dette automatisk."],
            ["Er momstallene gyldige for regnskap?", "Kalkulatoren er et hjelpeverktøy. Bruk alltid faktura og regnskapsprogrammet ditt for offisielle tall."]]},

    "laanekalkulator": {
        "kat": "finans",
        "navn": "Lånekalkulator", "icon": "🏦",
        "tittel": "Lånekalkulator – regn ut terminbeløp og total rente | Smartkalkulator",
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
            ["Hvordan regnes terminbeløpet ut?", "Kalkulatoren bruker annuitetslån: likt terminbeløp hver måned gjennom hele løpetiden, der renteandelen synker og avdragsgjelden øker over tid."],
            ["Hva er forskjellen på nominell og effektiv rente?", "Den nominelle renten er selve lånerenten. Den effektive inkluderer også gebyrer og etableringskostnad, og er derfor høyere. Kalkulatoren viser effektiv rente uten gebyrer."],
            ["Lønner det seg å betale ned raskere?", "Som regel ja – hver ekstra krone du betaler ned reduserer rentekostnaden for resten av løpetiden. Prøv å kutte løpetiden og se hvordan total rente faller."]]},

    "feriepenger": {
        "kat": "finans",
        "navn": "Feriepengeskalkulator", "icon": "🏖️",
        "tittel": "Feriepengeskalkulator – regn ut dine feriepenger | Smartkalkulator",
        "desc": "Gratis feriepengeskalkulator: finn hvor mange feriepenger du har opptjent basert på lønn og sats (10,2 % eller 12,2 %).",
        "intro": "Feriepenger = feriepengegrunnlaget ditt ganget med satsen. Skriv inn tallene og se beløpet med én gang.",
        "selects": [("sats", "Feriepengesats", [
            ["10.2", "Ordinær: 10,2 %"],
            ["12.2", "Over 60 år: 12,2 %"],
            ["10", "Kun 10 % (uten lovpålagt tillegg)"],
            ["12", "Kun 12 %"]], "10.2")],
        "inputs": [("lonn", "Feriepengegrunnlag / årslønn (kr)", "600000", "number")],
        "js": """var s=g('sats'), l=g('lonn'), fp=l*s/100;
return {stor: fmtK(fp), sub:'i feriepenger',
  celler:[['Sats',n1(s)+' %'],['Grunnlag',fmtK(l)]],
  rader:[['Feriepengegrunnlag',fmtK(l)],['Sats brukt',n1(s)+' %'],['Feriepenger utbetales',fmtK(fp)],['Svarer til per feriemåned',fmtK(fp/12)]]}""",
        "faq": [
            ["Hva er feriepenger?", "Feriepenger er en kompensasjon du tjener opp i løpet av året for å ha råd til ferien. De utbetales som regel i juni og utgjør 10,2 % av feriepengegrunnlaget (12,2 % for deg over 60 år)."],
            ["Hva er feriepengegrunnlaget?", "Alt du tjener i opptjeningsåret (1. september–31. august): lønn, bonus, provisjon og overtid. Skattefri godtgjørelse som reisepenger inngår ikke."],
            ["Hvorfor 10,2 % og ikke 10 %?", "Ferieloven gir 10 %, men den lovpålagte ferien er på 25 dager – tillegget på 2 prosentpoeng kompenserer for de fire ekstra dagene. Mange tariffavtaler gir 12 %."]]},

    "rentes-rente": {
        "kat": "finans",
        "navn": "Rentes rente-kalkulator", "icon": "📈",
        "tittel": "Rentes rente-kalkulator – se sparingen din vokse | Smartkalkulator",
        "desc": "Gratis kalkulator for rentes rente: se hva sparingen din blir verdt med engangsbeløp, månedlig innskudd og fast avkastning.",
        "intro": "Rentes rente betyr at avkastningen din også tjener avkastning. Skriv inn tallene og se hvordan sparingen komponerer seg.",
        "inputs": [("start", "Engangsbeløp nå (kr)", "100000", "number"),
                   ("mnd", "Månedlig sparing (kr)", "1000", "number"),
                   ("rente", "Årlig avkastning (%)", "5", "number"),
                   ("aar", "Antall år", "10", "number")],
        "js": """var p=g('start'), m=g('mnd'), r=g('rente')/100/12, n=g('aar')*12;
var fv=p*Math.pow(1+r,n)+(r>0?m*(Math.pow(1+r,n)-1)/r:m*n);
var inn=p+m*n;
return {stor: fmtK(fv), sub:'etter '+gs('aar')+' år',
  celler:[['Betalt inn',fmtK(inn)],['Avkastning',fmtK(fv-inn)]],
  rader:[['Sluttverdi',fmtK(fv)],['Totalt satt inn',fmtK(inn)],['Rentesavkastning',fmtK(fv-inn)],['Verdien er blitt',(inn>0?n0((fv/inn-1)*100)+' % av innskuddet':'–')]]}""",
        "faq": [
            ["Hva er rentes rente?", "At avkastningen din også begynner å tjene avkastning. Etter mange år blir dette den største bidragsyteren – derfor sier man at tidlig sparing slår stor sparing."],
            ["Hvilken avkastning kan jeg forvente?", "Historisk har globale aksjeindeksfond gitt ca. 7–8 % per år i snitt over lang tid, mens bankinnskudd gis 0–4 %. Ingen avkastning er garantert."],
            ["Hvorfor starter avkastningen så lavt?", "Rentebeløpene er små de første årene, men etter 15–20 år tar komponeringen av. Prøv å øke antall år og se forskjellen."]]},

    # ------------------------------------------------------------- bil og reise
    "elbil-ladekostnad": {
        "kat": "bil",
        "navn": "Elbilladekalkulator", "icon": "🔌",
        "tittel": "Elbilladekalkulator – kostnad for å lade elbil | Smartkalkulator",
        "desc": "Gratis kalkulator for elbillading: se strømkostnad per 100 km og per år, sammenlignet med en bensinbil.",
        "intro": "Basert på bilens forbruk og din strømpris. Sammenligning mot bensinbil kommer automatisk med.",
        "inputs": [("forbruk", "Elbil-forbruk (kWh/100 km)", "18", "number"),
                   ("pris", "Strømpris (kr/kWh)", "1.5", "number"),
                   ("km", "Km per år", "15000", "number"),
                   ("bforbruk", "Bensinbil-forbruk (L/100 km)", "6.5", "number"),
                   ("bpris", "Bensinpris (kr/L)", "21", "number")],
        "js": """var eb=g('forbruk')*g('pris'), ea=eb*g('km')/100;
var bb=g('bforbruk')*g('bpris'), ba=bb*g('km')/100;
return {stor: fmtK(ea), sub:'strøm per år',
  celler:[['Per 100 km (strøm)',fmtK(eb)],['Samme distanse bensin',fmtK(ba)]],
  rader:[['Elbil: strøm per år',fmtK(ea)],['Bensinbil samme distanse',fmtK(ba)],['Besparelse med elbil',fmtK(ba-ea)+' / år'],['Per 100 km',fmtK(eb)+' strøm vs '+fmtK(bb)+' bensin']]}""",
        "faq": [
            ["Hva koster det å lade elbil i Norge?", "Hjemme med vanlig strømpris rundt 1–1,5 kr/kWh koster 100 km typisk 18–30 kr. På hurtiglader kan prisen være 5–8 kr/kWh, altså vesentlig dyrere."],
            ["Bruker alle elbiler like mye strøm?", "Nei – de fleste moderne elbiler bruker 15–22 kWh per 100 km i blandet kjøring. Vinterkjøring kan øke forbruket med 20–40 %."],
            ["Er elbil fortsatt billigere enn bensin?", "Ja, normalt 3–5 ganger billigere i drivstoff. Husk likevel at forsikring og verditap kan være høyere for elbil."]]},

    # ------------------------------------------------------------- helse
    "kaloriberegner": {
        "kat": "livsstil",
        "navn": "Kaloriberegner", "icon": "🔥",
        "tittel": "Kaloriberegner – ditt daglige kaloriebehov | Smartkalkulator",
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
// kalorier, ikke kroner: n0 uten kronesuffiks
return {stor: n0(tdee), sub:'kcal per dag',
  celler:[['Hvileforbrenning',n0(bmr)+' kcal'],['Aktivitetsfaktor',gs('aktivitet')]],
  rader:[['Hvileforbrenning (BMR)',n0(bmr)+' kcal'],['Vedlikehold',n0(tdee)+' kcal'],
         ['Ned 0,5 kg/uke',n0(Math.max(tdee-500,1200))+' kcal'],['Opp 0,5 kg/uke',n0(tdee+500)+' kcal']]}""",
        "faq": [
            ["Hva er BMR?", "BMR (basal metabolic rate) er energien kroppen din forbrenner i full hvile. Det er størstedelen av det du forbrenner hver dag."],
            ["Hvor nøyaktig er kalkulatoren?", "Mifflin-St Jeor er den mest brukte formelen og treffer typisk innenfor ±10 % for de fleste. Individuelle variasjoner i muskelmasse og stoffskifte gir avvik."],
            ["Hvor mye skal jeg spise for å gå ned i vekt?", "Et vanlig og bærekraftig utgangspunkt er 500 kcal under vedlikeholdsbehov, som gir ca. 0,5 kg ned per uke. Ikke gå under 1 200 kcal uten legehjelp."]]},

    "proteinbehov": {
        "kat": "livsstil",
        "navn": "Proteinbehov-kalkulator", "icon": "💪",
        "tittel": "Proteinbehov-kalkulator – hvor mye protein per dag? | Smartkalkulator",
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
            ["Kan jeg få i meg for mye protein?", "For friske nyrefunksjoner er høyt inntak godt tolerert, men mer enn ca. 2,2 g/kg gir liten ekstra effekt. Nyresyke bør snakke med lege."],
            ["Beste kildene til protein?", "Fisk, kjøtt, egg, meieriprodukter, bønner og linser. En generell tommelfinger: 20–40 g protein per hovedmåltid dekker de fleste behov."]]},

    "bmikalkulator": {
        "kat": "livsstil",
        "navn": "BMI-kalkulator", "icon": "⚖️",
        "tittel": "BMI-kalkulator – regn ut din Body Mass Index | Smartkalkulator",
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

    # ------------------------------------------------------------- nyttige verktøy
    "prosentregner": {
        "kat": "hverdag",
        "navn": "Prosentregner", "icon": "％",
        "tittel": "Prosentregner – regn ut prosent raskt | Smartkalkulator",
        "desc": "Gratis prosentregner: finn prosentandel, endring i prosent og prosent av et tall. Enkle prosentregninger på sekunder.",
        "intro": "Skriv inn to verdier og få alle vanlige prosentregninger med én gang.",
        "inputs": [("a", "Verdi A", "50", "number"), ("b", "Verdi B", "200", "number")],
        "js": """var a=g('a'), b=g('b');
var pAB = b!==0 ? a/b*100 : NaN, pBA = a!==0 ? b/a*100 : NaN;
var endr = a!==0 ? (b-a)/Math.abs(a)*100 : NaN;
// A og B er generelle tall (ikke kroner): heltall vises rent, ellers én desimal
function tall(x){return Math.abs(x-Math.round(x))<0.005 ? n0(x) : n1(x)}
return {stor: isFinite(pAB)? n1(pAB)+' %' : '–', sub:'A er av B',
  celler:[['B er av A', isFinite(pBA)? n1(pBA)+' %':'–'],['A % av B som tall', isFinite(pAB)? tall(a/100*b):'–']],
  rader:[['A er '+(isFinite(pAB)?n1(pAB):'–')+' % av B',''],['B er '+(isFinite(pBA)?n1(pBA):'–')+' % av A',''],['Endring A til B', isFinite(endr)? (endr>=0?'+':'')+n1(endr)+' %':'–'],['A % brukt på B', tall(a/100*b)]]}""",
        "faq": [
            ["Hvordan regner jeg ut prosentøkning?", "(Ny verdi − gammel verdi) ÷ gammel verdi × 100. Skriver du inn gammel verdi som A og ny som B, viser kalkulatoren dette som «Endring A til B»."],
            ["Hvordan finner jeg X % av et tall?", "Multipliser tallet med prosenten delt på 100. Feltet «A % brukt på B» gjør akkurat dette."],
            ["Hva betyr prosentpoeng?", "Prosentpoeng er differansen mellom to prosenter. Fra 20 % til 25 % er det 5 prosentpoeng, men 25 % økning i relativ forstand."]]},

    "dato-kalkulator": {
        "kat": "hverdag",
        "navn": "Datokalkulator", "icon": "📅",
        "tittel": "Datokalkulator – dager mellom datoer | Smartkalkulator",
        "desc": "Gratis datokalkulator: finn antall dager mellom to datoer, eller legg til/trekk fra dager på en dato. Raskt og enkelt.",
        "intro": "Antall dager mellom to datoer, pluss en ny dato når du legger til N dager.",
        "inputs": [("fra", "Startdato", "", "date"),
                   ("til", "Sluttdato", "", "date"),
                   ("n", "Legg til dager på startdato", "30", "number")],
        "js": """function p(d){ return new Date(d+'T12:00:00'); }
var fs=gs('fra'), ts=gs('til'), f, t;
f = fs ? p(fs) : null;
t = ts ? p(ts) : null;
if(!f || isNaN(f)){ return {stor:'Velg startdato', sub:'', celler:[], rader:[]}; }
var ny = new Date(f.getTime()+g('n')*86400000);
var opts={day:'numeric',month:'short',year:'numeric'};
var df=f.toLocaleDateString('nb-NO',opts);
var dt=(t&&!isNaN(t))?t.toLocaleDateString('nb-NO',opts):null;
var dn=ny.toLocaleDateString('nb-NO',opts);
var dager = (t&&!isNaN(t)) ? Math.round((t-f)/86400000) : null;
return {stor: dager!==null ? n0(dager)+' dager' : dn, sub: dager!==null?'mellom datoene':'startdato + '+n0(g('n'))+' dager',
  celler:[['Uker', dager!==null? n1(dager/7):'–'],['Startdato', df]],
  rader:[['Startdato',df],['Sluttdato',dt||'–'],['Dager mellom',dager!==null?n0(dager):'–'],['Startdato + '+n0(g('n'))+' dager',dn]]}""",
        "faq": [
            ["Teller kalkulatoren med helger?", "Ja, alle dager telles med. Trenger du bare arbeidsdager, trekker du ca. 2/7 av dagene."],
            ["Kan jeg regne dager frem i tid?", "Ja – sett sluttdato fremover, eller bruk «legg til dager»-feltet for å få en ny dato direkte."],
            ["Stemmer det over tidssoner?", "Kalkulatoren bruker lokal dato ved middagstid for å unngå feil ved sommer-/vintertid."]]},

    "enhetskonverterer": {
        "kat": "hverdag",
        "navn": "Enhetskonverterer", "icon": "📐",
        "tittel": "Enhetskonverterer – lengde, vekt og temperatur | Smartkalkulator",
        "desc": "Konverter mellom enheter gratis: mm, cm, m, km, norske mil, pund, tonn, Celsius, Fahrenheit og mer. Raskt og enkelt.",
        "intro": "Skriv inn et tall og velg enheter – konverteringen skjer mens du taster.",
        "selects": [("fra", "Fra enhet", [
            ["mm", "millimeter"], ["cm", "centimeter"], ["m", "meter"], ["km", "kilometer"],
            ["mil", "norsk mil (10 km)"], ["mile", "engelsk mil"], ["tomme", "tomme"], ["fot", "fot"],
            ["g", "gram"], ["kg", "kilogram"], ["tonn", "tonn"], ["pund", "pund (lbs)"],
            ["C", "Celsius"], ["F", "Fahrenheit"], ["Kelvin", "Kelvin"]], "km"),
                    ("til", "Til enhet", [
            ["mm", "millimeter"], ["cm", "centimeter"], ["m", "meter"], ["km", "kilometer"],
            ["mil", "norsk mil (10 km)"], ["mile", "engelsk mil"], ["tomme", "tomme"], ["fot", "fot"],
            ["g", "gram"], ["kg", "kilogram"], ["tonn", "tonn"], ["pund", "pund (lbs)"],
            ["C", "Celsius"], ["F", "Fahrenheit"], ["Kelvin", "Kelvin"]], "mil")],
        "inputs": [("verdi", "Verdi", "5", "number")],
        "js": """var U={'mm':0.001,'cm':0.01,'m':1,'km':1000,'mil':10000,'mile':1609.344,'tomme':0.0254,'fot':0.3048};
var W={'g':0.001,'kg':1,'tonn':1000,'pund':0.45359237};
var T=['C','F','Kelvin'];
var v=g('verdi'), fra=gs('fra'), til=gs('til'), out=null;
function tc(x,u){return u==='C'?x:(u==='F'?(x-32)*5/9:x-273.15)}
function fc(c,u){return u==='C'?c:(u==='F'?c*9/5+32:c+273.15)}
if(T.indexOf(fra)>-1&&T.indexOf(til)>-1){ out=fc(tc(v,fra),til); }
else if(U[fra]&&U[til]){ out=v*U[fra]/U[til]; }
else if(W[fra]&&W[til]){ out=v*W[fra]/W[til]; }
if(out===null||isNaN(out)){ return {stor:'Velg to enheter av samme type',sub:'',celler:[],rader:[]}; }
var kat = T.indexOf(fra)>-1?'temperatur':(U[fra]?'lengde':'vekt');
return {stor:(Math.round(out*100)/100).toLocaleString('nb-NO')+' '+til, sub:kat,
  celler:[['Fra',fra+' ('+v+')'],['Til',til+' ('+(Math.round(out*100)/100)+')']],
  rader:[[v+' '+fra+' tilsvarer',(Math.round(out*10000)/10000).toLocaleString('nb-NO')+' '+til]]}""",
        "faq": [
            ["Hvor lang er en norsk mil?", "En norsk (skandinavisk) mil er nøyaktig 10 kilometer. Den engelske milen er 1,609344 km – pass på å ikke blande dem."],
            ["Hvordan regner jeg Celsius til Fahrenheit?", "Gang Celsius med 9, del på 5 og legg til 32: °F = °C × 9/5 + 32. Så 20 °C = 68 °F. Kalkulatoren gjør det automatisk."],
            ["Hvor mange pund er en kilo?", "Én kilogram = 2,20462 pund (lbs). Og én tomme = 2,54 cm, én fot = 30,48 cm."]]},

    "alder": {
        "kat": "hverdag",
        "navn": "Alderskalkulator", "icon": "🎂",
        "tittel": "Alderskalkulator – din eksakte alder i år, måneder og dager | Smartkalkulator",
        "desc": "Gratis alderskalkulator: finn din eksakte alder i år, måneder og dager – pluss levede dager og dager til neste bursdag.",
        "intro": "Skriv inn fødselsdatoen din og få eksakt alder, antall levede dager og nedtelling til neste bursdag.",
        "inputs": [("fdato", "Fødselsdato", "", "date")],
        "js": """var bs=gs('fdato');
if(!bs){return {stor:'Velg fødselsdato',sub:'',celler:[],rader:[]}}
var f=new Date(bs+'T12:00:00'), t=new Date();
if(isNaN(f)||f>t){return {stor:'Ugyldig dato',sub:'',celler:[],rader:[]}}
var y=t.getFullYear()-f.getFullYear(), m=t.getMonth()-f.getMonth(), d=t.getDate()-f.getDate();
if(d<0){m--;d+=new Date(t.getFullYear(),t.getMonth(),0).getDate()}
if(m<0){y--;m+=12}
var dager=Math.floor((t-f)/86400000);
var nb=new Date(t.getFullYear(),f.getMonth(),f.getDate(),12);
if(nb<=t){nb.setFullYear(t.getFullYear()+1)}
var tilbd=Math.ceil((nb-t)/86400000);
return {stor:y+' år', sub:'og '+m+' mnd, '+d+' dager',
  celler:[['Levd i dager',n0(dager)],['Til neste bursdag',n0(tilbd)+' dager']],
  rader:[['Eksakt alder',y+' år, '+m+' måneder, '+d+' dager'],['Levd totalt',n0(dager)+' dager (ca. '+n0(Math.floor(dager/7))+' uker)'],['Dager til neste bursdag',n0(tilbd)+' dager']]}""",
        "faq": [
            ["Hvordan beregnes eksakt alder?", "Vi teller hele år fra fødselsdato, deretter hele måneder, så resterende dager. Månelengden varierer, så vi bruker faktiske kalendermåneder."],
            ["Hvorfor står det «ca.» uker?", "En uke er alltid 7 dager; tallet stemmer helt for dagen du sjekker. «Ca.» gjelder bare at antall dager endrer seg fra dag til dag."],
            ["Kan jeg regne på andre enn meg selv?", "Ja – hvilken som helst fødselsdato fungerer, f.eks. barn, familiemedlemmer eller en bedriftens stiftelsesdato."]]},
    "bilkostnadskalkulator": {
        "kat": "bil",
        "navn": "Bilkostnadskalkulator", "icon": "🚗",
        "tittel": "Bilkostnadskalkulator – hva koster bilen din per måned? | Smartkalkulator",
        "desc": "Gratis kalkulator for totale bilkostnader i Norge: forsikring, drivstoff, årsavgift, bom, vedlikehold og verditap. Se kostnad per måned og per km.",
        "intro": "Alle bilens kostnader i én utregning: fyll inn tallene dine og se hva bilen egentlig koster per måned og per kilometer.",
        "inputs": [("fors", "Forsikring (kr/år)", "6000", "number"),
                   ("kmaar", "Km per år", "12000", "number"),
                   ("forbruk", "Forbruk (L eller kWh per 100 km)", "6.0", "number"),
                   ("pris", "Pris per enhet (kr/L eller kr/kWh)", "22", "number"),
                   ("aars", "Årsavgift + trafikkforsikringsavgift (kr/år)", "4500", "number"),
                   ("bom", "Bom, parkering (kr/år)", "2000", "number"),
                   ("serv", "Service, dekk, reparasjoner (kr/år)", "5000", "number"),
                   ("tap", "Verditap / avdrag (kr/år)", "30000", "number")],
        "js": """var post={Forsikring:g('fors'),Drivstoff:g('kmaar')/100*g('forbruk')*g('pris'),'Årsavgift':g('aars'),'Bom/parkering':g('bom'),Vedlikehold:g('serv'),'Verditap/avdrag':g('tap')};
var tot=0,top='–',topV=-1;
for(var k in post){tot+=post[k];if(post[k]>topV){topV=post[k];top=k}}
var km=g('kmaar');
return {stor: fmtK(tot/12), sub:'per måned',
  celler:[['Per år',fmtK(tot)],['Per km',km>0?(Math.round(tot/km*100)/100).toLocaleString('nb-NO')+' kr':'–']],
  rader:Object.keys(post).map(function(k){return [k,fmtK(post[k])+' / år ('+fmtK(post[k]/12)+'/mnd)']}).concat([['Største kostnad',top],['TOTALT',fmtK(tot)+' / år']])}""",
        "faq": [
            ["Hva koster det å ha bil per måned i Norge?", "En typisk norsk bil koster mellom 5 000 og 12 000 kroner per måned alt inkludert. De største postene er verditap, forsikring og drivstoff. Fyll ut feltene for å se ditt eget tall."],
            ["Hva er årsavgiften for en bil?", "Basisårsavgiften for personbil er 3 074 kroner per år (2026). Dieselbiler uten partikkelfilter betaler tillegg, og trafikkforsikringsavgift kommer i tillegg – variere etter utslipp."],
            ["Hvorfor skal jeg ta med «verditap»?", "Bilen mister verdi hver måned selv om du ikke bruker den. Har du finansiering, kan du i stedet legge inn avdragene – begge deler er reelle kostnader ved å eie bilen."]]},

    # ------------------------------------------------------------- hverdag
    "rabattkalkulator": {
        "kat": "hverdag",
        "navn": "Rabattkalkulator", "icon": "🏷️",
        "tittel": "Rabattkalkulator – hvor mye sparer du? | Smartkalkulator",
        "desc": "Gratis rabattkalkulator: regn ut hvor mye du sparer i kroner og hva den faktiske prosenten blir når to eller flere tilbud slås sammen.",
        "intro": "Slår butikken sammen to tilbud? Finn ut hva du faktisk sparer i kroner og hva den reelle prosenten blir.",
        "inputs": [("pris", "Opprinnelig pris (kr)", "1000", "number"),
                   ("rab1", "Rabatt 1 (%)", "20", "number"),
                   ("rab2", "Rabatt 2 (%) – valgfri", "10", "number")],
        "js": """var p=g('pris'),r1=g('rab1')/100,r2=g('rab2')/100;
var ny=p*(1-r1)*(1-r2);
var spart=p-ny;
var tot=r1+r2-r1*r2;
return {stor: fmtK(spart)+' kr', sub:'totalt i besparelse',
  celler:[['Ny pris',fmtK(Math.round(ny))+' kr'],['Reell rabatt',Math.round(tot*100)+' %']],
  rader:[['Opprinnelig',fmtK(p)+' kr'],['Du betaler',fmtK(Math.round(ny))+' kr'],['Du sparer',fmtK(Math.round(spart))+' kr'],['Reell rabatt',Math.round(tot*100)+' %']]}""",
        "faq": [
            ["Hvordan regnes to rabatter sammen?", "Rabatter slås ikke enkelt sammen til 30 %. Først trekkes 20 % av prisen, deretter 10 % av det nye beløpet. Reell rabatt blir 28 %, ikke 30 %."],
            ["Er det bedre å få én stor eller to små rabatter?", "Det blir nesten alltid litt mer å få én rabatt på 30 % enn 20 % + 10 %, fordi den andre rabatten kun gjelder det allerede reduserte beløpet."]]},

    "termindato": {
        "kat": "hverdag",
        "navn": "Termindato-kalkulator", "icon": "🗓️",
        "tittel": "Termindato-kalkulator – når er fristen? | Smartkalkulator",
        "desc": "Gratis termindato-kalkulator: legg inn startdato og antall dager, og se hvilken dato en frist eller periode utløper.",
        "intro": "Fristen er X dager fra i dag – men hvilken dato er det? Fyll inn startdato og antall dager, så regner vi ut når det er ferdig.",
        "inputs": [("start", "Startdato", "", "date"),
                   ("dager", "Antall dager til frist", "14", "number")],
        "js": """var s=g('start'),d=g('dager');
if(!s) return {stor:'–',sub:'fyll inn startdato'};
var dt=new Date(s+'T00:00:00');
dt.setDate(dt.getDate()+d);
var opt={weekday:'long',day:'numeric',month:'long',year:'numeric'};
var txt=dt.toLocaleDateString('nb-NO',opt);
var iDag=new Date();iDag.setHours(0,0,0,0);
var diff=Math.round((dt-iDag)/86400000);
return {stor: txt[0].toUpperCase()+txt.slice(1), sub:(diff>=0?diff+' dager til':'var '+Math.abs(diff)+' dager siden'),
  celler:[['Startdato',new Date(s+'T00:00:00').toLocaleDateString('nb-NO',{day:'numeric',month:'long',year:'numeric'})],['Antall dager',d+' dager']],
  rader:[['Startdato',new Date(s+'T00:00:00').toLocaleDateString('nb-NO',{day:'numeric',month:'long',year:'numeric'})],['Legg til',d+' dager'],['Fristen er',txt[0].toUpperCase()+txt.slice(1)]]}""",
        "faq": [
            ["Teller termindagen med?", "Vi legger antall dager rett til startdatoen – så 14 dager fra 1. januar er 15. januar. Det matcher hvordan de fleste frister (f.eks. angrerett) faktisk regnes."],
            ["Kan jeg regne bakover?", "Ja – fyll inn et negativt antall dager (f.eks. -30) for å finne en dato tidligere i tid."]]},

    "sovnsyklus": {
        "kat": "livsstil",
        "navn": "Søvnsyklus-kalkulator", "icon": "😴",
        "tittel": "Søvnsyklus-kalkulator – når bør du vekkes? | Smartkalkulator",
        "desc": "Gratis søvnsyklus-kalkulator: finn ut når du bør legge deg eller vekkes for å våkne etter et helt antall søvnsykluser (ca. 90 min hver).",
        "intro": "En søvnsyklus varer ca. 90 minutter. Våkner du midt i en, er du tung i hodet – denne kalkulatoren finner gode legge- og vekketidspunkter.",
        "inputs": [("vekk", "Ønsket vekketid", "07:00", "time"),
                   ("sykluser", "Antall søvnsykluser", "5", "number")],
        "js": """var v=g('vekk').split(':'),syk=g('sykluser');
var dt=new Date();dt.setHours(+v[0],+v[1],0,0);
var total=syk*90;
var legg=new Date(dt.getTime()-total*60000);
var hh=('0'+legg.getHours()).slice(-2),mm=('0'+legg.getMinutes()).slice(-2);
return {stor: hh+':'+mm, sub:'bør du legge deg',
  celler:[['Søvnsykluser',syk+' stk'],['Søvn i timer',(total/60).toFixed(1)+' t']],
  rader:[['Ønsket vekketid',g('vekk')],['Antall sykluser',syk+' × 90 min'],['Anbefalt leggetid',hh+':'+mm],['Planlagt søvn',(total/60).toFixed(1)+' timer']]}""",
        "faq": [
            ["Hvor lenge varer en søvnsyklus?", "Omtrent 90 minutter for en voksen. En hel natt består av 4–6 slike sykluser med veksling mellom lett, dyp og REM-søvn."],
            ["Hvorfor vil jeg våkne mellom sykluser?", "Du er lettest å vekke rett etter en syklus er ferdig. Våkner du midt i en dyp fase, føler du deg tung og uklar – såkalt søvninnøling."]]},

    "pris-per-kilo": {
        "kat": "hverdag",
        "navn": "Pris per kilo-kalkulator", "icon": "⚖️",
        "tittel": "Pris per kilo – sammenlign handlepriser | Smartkalkulator",
        "desc": "Gratis pris-per-kilo-kalkulator: sammenlign to varer med ulik vekt og pris, og finn ut hvilken som faktisk er billigst per kilo.",
        "intro": "To pakker, ulik vekt og ulik pris – hvilken er egentlig billigst? Fyll inn begge, så regner vi ut pris per kilo og hvem som vinner.",
        "inputs": [("p1", "Pris vare A (kr)", "45", "number"),
                   ("w1", "Vekt vare A (gram)", "500", "number"),
                   ("p2", "Pris vare B (kr)", "79", "number"),
                   ("w2", "Vekt vare B (gram)", "1000", "number")],
        "js": """var p1=g('p1'),w1=g('w1')/1000,p2=g('p2'),w2=g('w2')/1000;
if(w1<=0||w2<=0) return {stor:'–',sub:'vekt må være over 0'};
var k1=p1/w1,k2=p2/w2;
var billig=k1<=k2?'A':'B';
return {stor: fmtK(Math.min(k1,k2))+' kr', sub:'billigst per kilo (vare '+billig+')',
  celler:[['Vare A',Math.round(k1*100)/100+' kr/kg'],['Vare B',Math.round(k2*100)/100+' kr/kg']],
  rader:[['Vare A',fmtK(p1)+' kr / '+g('w1')+' g → '+Math.round(k1*100)/100+' kr/kg'],['Vare B',fmtK(p2)+' kr / '+g('w2')+' g → '+Math.round(k2*100)/100+' kr/kg'],['Billigst',(billig==='A'?'Vare A':'Vare B')+' sparer '+fmtK(Math.abs(k1-k2))+' kr/kg']]}""",
        "faq": [
            ["Hvorfor sjekke pris per kilo?", "Butikker markedsfører ofte «tilbud» på store pakker som i realiteten er dyrere per kilo enn en mindre pakke. Å regne på kiloprisen avslører det."],
            ["Hva med literspris?", "Samme prinsipp gjelder for varer målt i liter (f.eks. oppvaskmiddel) – bytt gram mot milliliter i hodet, regnestykket er det samme."]]},

}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITTEL__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="https://arneshodzic.github.io/seo-verktoy/verktoy/__MAPPE__/">
<meta name="theme-color" content="#060a14">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Smartkalkulator">
<meta property="og:locale" content="nb_NO">
<meta property="og:title" content="__TITTEL__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="https://arneshodzic.github.io/seo-verktoy/verktoy/__MAPPE__/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 96 96'%3E%3Cg transform='rotate(-7 48 48)'%3E%3Cpath d='M32 11h25.2L75 28.8V74a11 11 0 0 1-11 11H32a11 11 0 0 1-11-11V22a11 11 0 0 1 11-11z' fill='%23101a2c' stroke='%2322d3ee' stroke-width='4'/%3E%3Crect x='30' y='21.5' width='36' height='17' rx='4.5' fill='%2305202a' stroke='%2322d3ee' stroke-width='2.5'/%3E%3Cpath d='M13.6 2 4.9 14.4h5.5L8.6 22l8.9-12.6h-5.6z' transform='translate(41.4 24.2) scale(.56)' fill='%2367e8f9'/%3E%3Cg fill='%232b3a54'%3E%3Crect x='30' y='48' width='11' height='9' rx='2.5'/%3E%3Crect x='44' y='48' width='11' height='9' rx='2.5'/%3E%3Crect x='30' y='62' width='11' height='9' rx='2.5'/%3E%3C/g%3E%3Crect x='44' y='62' width='11' height='9' rx='2.5' fill='%2322d3ee'/%3E%3C/g%3E%3C/svg%3E">
<script type="application/ld+json">__SCHEMA_APP__</script>
<script type="application/ld+json">__SCHEMA_FAQ__</script>
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
body{
  font-family:Inter,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--txt);
  line-height:1.65;font-size:16px;padding:0 1rem 3rem;overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
/* levende bakgrunn: to auraer + svakt rutenett som fader ut */
body::before,body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none}
body::before{background:
  radial-gradient(900px 520px at 10% -10%,rgba(34,211,238,.17),transparent 62%),
  radial-gradient(760px 470px at 94% 2%,rgba(129,140,248,.15),transparent 64%),
  linear-gradient(180deg,#080f1e,#060a14 46%)}
body::after{
  opacity:.5;
  background-image:linear-gradient(rgba(150,185,255,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(150,185,255,.055) 1px,transparent 1px);
  background-size:58px 58px;
  -webkit-mask-image:radial-gradient(72% 52% at 50% 0%,#000,transparent);
          mask-image:radial-gradient(72% 52% at 50% 0%,#000,transparent);
}
.wrap{max-width:1040px;margin:0 auto}
a{color:var(--acc-lys);text-underline-offset:3px}
a:hover{color:#fff}
:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:6px}

/* ---------- topplinje ---------- */
.topp{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1.05rem 0 .35rem}
.merke{display:inline-flex;align-items:center;gap:.55rem;text-decoration:none;color:#fff;
  font-family:Sora,Inter,sans-serif;font-weight:700;font-size:1.05rem;letter-spacing:-.02em}
.merke svg{width:30px;height:30px;flex:0 0 auto;filter:drop-shadow(0 0 9px rgba(34,211,238,.45))}
.merke span{white-space:nowrap}
.merke i{font-style:normal;color:var(--acc)}
.merke:hover{color:#fff}
.pil{display:inline-flex;align-items:center;gap:.4rem;text-decoration:none;white-space:nowrap;
  font-size:.85rem;font-weight:500;color:var(--mut);padding:.45rem .85rem;border-radius:999px;
  border:1px solid var(--line);background:rgba(255,255,255,.03);transition:.18s}
.pil:hover{color:#fff;border-color:rgba(34,211,238,.5);background:rgba(34,211,238,.08)}

/* ---------- hero ---------- */
.hero{padding:1.6rem 0 1.4rem}
h1{font-family:Sora,Inter,sans-serif;font-weight:700;font-size:clamp(1.6rem,6.2vw,2.4rem);
  line-height:1.14;letter-spacing:-.035em;color:#fff;display:flex;align-items:center;gap:.7rem;flex-wrap:wrap}
h1 .ico{width:2.7rem;height:2.7rem;flex:0 0 auto;display:inline-grid;place-items:center;font-size:1.35rem;
  border-radius:15px;border:1px solid rgba(34,211,238,.3);
  background:linear-gradient(158deg,rgba(34,211,238,.2),rgba(129,140,248,.13));
  box-shadow:0 0 24px -6px rgba(34,211,238,.45)}
.intro{color:var(--mut);margin-top:.85rem;max-width:64ch;font-size:1.03rem}
.marker{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.05rem}
.marker span{font-size:.75rem;font-weight:500;color:var(--dim);padding:.28rem .65rem;border-radius:999px;
  border:1px solid var(--line);background:rgba(255,255,255,.025)}

/* ---------- kort ---------- */
.card{position:relative;background:linear-gradient(168deg,var(--card-a),var(--card-b));
  border:1px solid var(--line);border-radius:var(--r);padding:1.2rem;box-shadow:var(--skygge)}
.korttittel{font-family:Sora,Inter,sans-serif;font-size:.98rem;font-weight:600;color:#fff;margin-bottom:.95rem}
h2{font-family:Sora,Inter,sans-serif;font-weight:600;font-size:1.15rem;color:#fff;letter-spacing:-.015em}

/* ---------- kalkulator-oppsett (mobil først) ---------- */
.kalk{display:grid;gap:.9rem;align-items:start}
.res{order:-1}
@media(min-width:880px){
  .kalk{grid-template-columns:1.05fr .95fr}
  .res{order:0;position:sticky;top:1.1rem}
  /* rolig lesekolonne under kalkulatoren */
  .detalj,.faq,.cta,footer{max-width:800px;margin-left:auto;margin-right:auto}
}

/* ---------- resultat ---------- */
.res{overflow:hidden;text-align:left;padding:1.4rem 1.25rem;border-color:rgba(34,211,238,.34);
  background:linear-gradient(152deg,rgba(8,54,72,.9),rgba(12,23,45,.95) 56%,rgba(38,32,90,.72));
  box-shadow:0 0 0 1px rgba(34,211,238,.07),0 34px 64px -44px rgba(34,211,238,.6)}
.res::before{content:'';position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(125% 78% at 50% -12%,rgba(34,211,238,.24),transparent 64%)}
.res>*{position:relative}
.res::after{content:'';position:absolute;left:0;right:0;top:0;height:1px;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(103,232,249,.85),transparent)}
.eyebrow{display:block;font-size:.7rem;font-weight:600;letter-spacing:.17em;text-transform:uppercase;color:var(--acc-lys)}
.big{font-family:Sora,Inter,sans-serif;font-weight:700;font-size:clamp(2.3rem,11vw,3.4rem);line-height:1.04;
  letter-spacing:-.04em;color:#fff;font-variant-numeric:tabular-nums;margin-top:.4rem;word-break:break-word;
  text-shadow:0 0 36px rgba(34,211,238,.34)}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
  .big{background:linear-gradient(178deg,#fff 38%,#a5f3fc);-webkit-background-clip:text;background-clip:text;
    -webkit-text-fill-color:transparent}
}
.sub{color:#9fe3f5;font-size:.96rem;margin-top:.3rem;min-height:1.2em}
.row3{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:.55rem;margin-top:1.25rem}
.cell{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.09);border-radius:var(--r-s);
  padding:.65rem .7rem;animation:inn .42s both}
.cell span{display:block;font-size:.68rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:#a8cfde}
.cell b{display:block;font-family:Sora,Inter,sans-serif;font-weight:600;font-size:1.05rem;color:#fff;
  font-variant-numeric:tabular-nums;margin-top:.2rem;letter-spacing:-.02em}

/* ---------- felter ---------- */
#felt{display:grid;grid-template-columns:1fr;gap:.9rem}
@media(min-width:520px){#felt{grid-template-columns:repeat(auto-fit,minmax(195px,1fr))}}
#felt label{display:block;font-size:.79rem;font-weight:600;letter-spacing:.01em;color:var(--mut);margin-bottom:.38rem}
#felt input,#felt select{width:100%;min-height:48px;padding:.7rem .85rem;border-radius:var(--r-s);
  border:1px solid var(--line-2);background-color:#080e1c;color:#fff;font:inherit;font-size:1.02rem;
  font-variant-numeric:tabular-nums;color-scheme:dark;transition:border-color .18s,box-shadow .18s,background-color .18s}
#felt input:hover,#felt select:hover{border-color:#456485}
#felt input:focus,#felt select:focus{outline:2px solid var(--acc);outline-offset:2px;border-color:var(--acc);
  background-color:#0a1526;box-shadow:0 0 0 4px rgba(34,211,238,.13)}
#felt select{-webkit-appearance:none;appearance:none;padding-right:2.5rem;cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='9' viewBox='0 0 14 9'%3E%3Cpath d='M1 1l6 6 6-6' fill='none' stroke='%2322d3ee' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right .95rem center}

/* ---------- detaljer ---------- */
.detalj{margin-top:.9rem}
.detalj table{width:100%;border-collapse:collapse;font-size:.95rem}
.detalj tr{animation:inn .34s both}
.detalj td{padding:.66rem .15rem;border-bottom:1px solid var(--line)}
.detalj tr:last-child td{border-bottom:0}
.detalj td:first-child{color:var(--mut)}
.detalj td:last-child{text-align:right;color:#fff;font-weight:600;font-variant-numeric:tabular-nums;padding-left:.6rem}

/* ---------- FAQ ---------- */
.faq{margin-top:.9rem}
.faq h2{margin-bottom:.9rem}
.faq details{color:var(--mut);font-size:.95rem;border:1px solid var(--line);border-radius:var(--r-s);
  background:rgba(255,255,255,.022);margin-bottom:.55rem;padding:0 1rem .95rem;transition:border-color .18s}
.faq details:not([open]){padding-bottom:0}
.faq details[open]{border-color:rgba(34,211,238,.32);background:rgba(34,211,238,.045)}
.faq summary{list-style:none;cursor:pointer;position:relative;margin:0 -1rem;padding:.9rem 2.8rem .9rem 1rem;
  font-weight:600;color:#fff;font-size:.97rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'';position:absolute;right:1.15rem;top:50%;width:8px;height:8px;
  border-right:2px solid var(--acc);border-bottom:2px solid var(--acc);
  transform:translateY(-70%) rotate(45deg);transition:transform .22s}
.faq details[open] summary::after{transform:translateY(-25%) rotate(225deg)}
.faq summary:hover{color:var(--acc-lys)}

/* ---------- CTA + bunn ---------- */
.cta{margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:.9rem;align-items:center;justify-content:space-between;
  padding:1.15rem 1.2rem;border-radius:var(--r);border:1px solid var(--line);
  background:linear-gradient(120deg,rgba(34,211,238,.09),rgba(129,140,248,.07))}
.cta p{color:var(--mut);font-size:.95rem}
.cta strong{color:#fff;font-family:Sora,Inter,sans-serif}
.knapp{display:inline-flex;align-items:center;gap:.45rem;text-decoration:none;font-weight:600;font-size:.94rem;
  color:#04212b;background:linear-gradient(180deg,#67e8f9,#22d3ee);padding:.72rem 1.25rem;border-radius:999px;
  box-shadow:0 12px 26px -14px rgba(34,211,238,.85);transition:transform .16s,box-shadow .16s}
.knapp:hover{color:#04212b;transform:translateY(-1px);box-shadow:0 16px 30px -12px rgba(34,211,238,.95)}
footer{margin-top:2.2rem;padding-top:1.2rem;border-top:1px solid var(--line);color:var(--dim);font-size:.83rem;
  display:flex;flex-wrap:wrap;gap:.5rem;justify-content:space-between}
.skjult{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

@keyframes inn{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
@keyframes glo{from{text-shadow:0 0 44px rgba(34,211,238,.8)}to{text-shadow:0 0 36px rgba(34,211,238,.34)}}
.big.puls{animation:glo .6s ease-out}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
@media(max-width:400px){
  body{padding:0 .8rem 2.5rem}
  .card{padding:1.05rem}.res{padding:1.25rem 1.05rem}
  .cta{padding:1rem}.knapp{width:100%;justify-content:center}
}
</style>
</head>
<body>
<div class="wrap">

<header class="topp">
  <a class="merke" href="../../" aria-label="Smartkalkulator – forsiden">
    <svg viewBox="0 0 96 96" aria-hidden="true" focusable="false">
      <g transform="rotate(-7 48 48)">
        <path d="M32 11h25.2L75 28.8V74a11 11 0 0 1-11 11H32a11 11 0 0 1-11-11V22a11 11 0 0 1 11-11z"
              fill="#111a2b" stroke="#22d3ee" stroke-width="3.4" stroke-linejoin="round"/>
        <rect x="30" y="21.5" width="36" height="17" rx="4.5" fill="#05202a" stroke="#22d3ee" stroke-width="2.2"/>
        <path d="M13.6 2 4.9 14.4h5.5L8.6 22l8.9-12.6h-5.6z" transform="translate(41.4 24.2) scale(.56)" fill="#67e8f9"/>
        <g fill="#2b3a54">
          <rect x="30" y="48" width="11" height="9" rx="2.6"/><rect x="44" y="48" width="11" height="9" rx="2.6"/>
          <rect x="30" y="62" width="11" height="9" rx="2.6"/>
        </g>
        <rect x="44" y="62" width="11" height="9" rx="2.6" fill="#22d3ee"/>
      </g>
    </svg>
    <span>Smart<i>kalkulator</i></span>
  </a>
  <a class="pil" href="../../">Alle kalkulatorer &#8594;</a>
</header>

<main>
<div class="hero">
  <h1><span class="ico" aria-hidden="true">__ICON__</span>__NAVN__</h1>
  <p class="intro">__INTRO__</p>
  <div class="marker"><span>Gratis</span><span>Ingen registrering</span><span>Ingen sporing</span><span>Oppdatert __DATO__</span></div>
</div>

<section class="kalk">
  <div class="card">
    <h2 class="korttittel">Dine tall</h2>
    <div class="grid" id="felt">__FELT__</div>
    <noscript><p style="color:#fca5a5;font-size:.88rem;margin-top:.9rem">Kalkulatoren krever JavaScript for å regne ut resultatet.</p></noscript>
  </div>

  <div class="card res">
    <span class="eyebrow">Resultat</span>
    <div class="big" id="stor">&ndash;</div>
    <div class="sub" id="sub"></div>
    <div class="row3" id="celler"></div>
  </div>
</section>

<section class="card detalj">
  <h2 class="korttittel">Detaljer</h2>
  <table><tbody id="rader"></tbody></table>
</section>
<p class="skjult" id="lest" role="status" aria-live="polite"></p>

<section class="card faq">
  <h2>Ofte spurt</h2>
  __FAQ__
</section>

<div class="cta">
  <p><strong>Trenger du å regne ut noe annet?</strong><br>Vi har kalkulatorer for finans, bil, helse og hverdag.</p>
  <a class="knapp" href="../../">Alle kalkulatorer &#8594;</a>
</div>
</main>

<footer>
  <span>Smartkalkulator &middot; gratis &middot; ingen reklame &middot; ingen sporing</span>
  <span>Oppdatert __DATO__</span>
</footer>
</div>

<script>
(function(){
var doc=document;
var redusert=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var eStor=doc.getElementById('stor'),eSub=doc.getElementById('sub'),
    eCeller=doc.getElementById('celler'),eRader=doc.getElementById('rader'),eLest=doc.getElementById('lest');

function g(id){return parseFloat(doc.getElementById(id).value)||0}
function gs(id){return doc.getElementById(id).value}
function n0(x){return Math.round(x).toLocaleString('nb-NO')}
function n1(x){return (Math.round(x*10)/10).toLocaleString('nb-NO',{minimumFractionDigits:1,maximumFractionDigits:1})}
function fmtK(x){return n0(x)+' kr'}

/* Tell-opp: finner første tall i strengen, animerer det og beholder tekst rundt ("kr", "/ mnd", "%"). */
var TALL=/-?\d(?:[\d\s]*\d)?(?:,\d+)?/;   /* JS \s dekker vanlig mellomrom, NBSP og smalt NBSP */
function fmtD(v,d){return v.toLocaleString('nb-NO',{minimumFractionDigits:d,maximumFractionDigits:d})}
function settTall(el,verdi){
  var s=(verdi==null?'':String(verdi)),m=s.match(TALL);
  if(el._raf){cancelAnimationFrame(el._raf);el._raf=0}
  if(!m){el.textContent=s;el._v=null;return}
  var raw=m[0],pre=s.slice(0,m.index),post=s.slice(m.index+raw.length),
      mal=parseFloat(raw.replace(/\s/g,'').replace(',','.')),
      des=raw.indexOf(',')>-1?raw.length-raw.indexOf(',')-1:0;
  if(!isFinite(mal)){el.textContent=s;el._v=null;return}
  var fra=(el._v==null?0:el._v);
  el._v=mal;
  if(redusert||Math.abs(mal-fra)<.005){el.textContent=pre+fmtD(mal,des)+post;return}
  var t0=0;
  function steg(t){
    if(!t0){t0=t}
    var p=Math.min(1,(t-t0)/460),e=1-Math.pow(1-p,3);
    el.textContent=pre+fmtD(fra+(mal-fra)*e,des)+post;
    if(p<1){el._raf=requestAnimationFrame(steg)}
    else{el._raf=0;el.textContent=pre+fmtD(mal,des)+post}
  }
  el._raf=requestAnimationFrame(steg);
}

function tegnCeller(liste){
  if(eCeller.children.length!==liste.length){
    eCeller.innerHTML='';
    liste.forEach(function(_,i){
      var d=doc.createElement('div');d.className='cell';d.style.animationDelay=(i*70)+'ms';
      d.appendChild(doc.createElement('span'));d.appendChild(doc.createElement('b'));
      eCeller.appendChild(d);
    });
  }
  liste.forEach(function(x,i){
    var d=eCeller.children[i];
    d.children[0].textContent=x[0];
    settTall(d.children[1],x[1]);
  });
}
function tegnRader(liste){
  if(eRader.children.length!==liste.length){
    eRader.innerHTML='';
    liste.forEach(function(_,i){
      var tr=doc.createElement('tr');tr.style.animationDelay=(i*45)+'ms';
      tr.appendChild(doc.createElement('td'));tr.appendChild(doc.createElement('td'));
      eRader.appendChild(tr);
    });
  }
  liste.forEach(function(x,i){
    var tr=eRader.children[i];
    tr.children[0].textContent=x[0];
    tr.children[1].textContent=(x[1]==null?'':x[1]);
  });
}

var lesTid;
function beregn(){
  var r=(function(){
__JS__
  })();
  if(!r){return}
  if(r.stor!=null){settTall(eStor,r.stor)}
  eSub.textContent=(r.sub==null?'':r.sub);
  tegnCeller(r.celler||[]);
  tegnRader(r.rader||[]);
  if(!redusert){eStor.classList.remove('puls');void eStor.offsetWidth;eStor.classList.add('puls')}
  clearTimeout(lesTid);
  lesTid=setTimeout(function(){eLest.textContent=((r.stor||'')+' '+(r.sub||'')).trim()},700);
}

doc.querySelectorAll('#felt input,#felt select').forEach(function(f){
  f.addEventListener('input',beregn);
  f.addEventListener('change',beregn);
});
beregn();
})();
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
        felt += (f'<div><label for="{sid}">{_esc(label)}</label>'
                 f'<select id="{sid}" name="{sid}">{opts}</select></div>\n')
    for iid, label, default, typ in spec.get("inputs", []):
        felt += (f'<div><label for="{iid}">{_esc(label)}</label>'
                 f'<input type="{typ}" id="{iid}" name="{iid}" value="{default}" '
                 f'inputmode="{"decimal" if typ == "number" else "text"}"></div>\n')
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
