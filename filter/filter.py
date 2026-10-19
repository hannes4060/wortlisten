#!/usr/bin/env python3
"""Entfernt Wörter mit potenziell heiklen / zweideutigen Bestandteilen aus Wortlisten.

Aufruf: filter.py <eingabe> <ausgabe_behalten> <ausgabe_entfernt> [filter/manuell.txt]
Abgleich: Teilstring, ohne Groß/Kleinschreibung. Ausnahmen werden vorher aus dem Wort
herausgeschnitten (z. B. "kanal" bevor nach "anal" gesucht wird).
"""
import re
import sys

STAEMME = {
    "Krankheit/Medizin": """
        krebs tumor karzinom metasta chemo onkolog leukaem leukam aids hiv demenz alzheimer
        parkinson epilep diabet schlaganfall infarkt tuberkul  seuche pandem epidem corona
        covid virus infekt infiz impf krank siech therap diagnos patient klinik hospiz palliativ
        intensivstation notaufnahme notarzt amputat prothese rollstuhl behindert gelaehm laehm
        lahm invalid pflegefall pflegeheim altersheim beatm koma lepra syphilis tripper herpes
        aussatz eitrig geschwuer geschwur warze laeuse kraetze senil gebrechlich krueppel
        kruppel inkontinen prostata hoden menstru tampon erbrech erbroch kotz durchfall impoten
        blut glatz narkose
    """,
    "Psyche/Sucht/Essstörung": """
        depress burnout psych schizo bipolar manisch neurot trauma angst panik phobie
        wahnsinn irrsinn irrenanstalt heilanstalt klapse magersucht bulimi anorex essstoer essstor uebergewicht
        ubergewicht adipos diaet diat abnehm kalorie hungern abmager suechtig suchtig droge
        heroin kokain koks cannabis haschisch kiffe alkohol saeufer saufen besoffen rauschgift
        entzug verzweif hoffnungslos einsam ritzen
    """,
    "Schwangerschaft/Familie/Trennung": """
        fehlgeburt totgeburt fruehgeburt abtreib abort unfruchtbar schwanger kinderlos
        kinderwunsch scheidung sorgerecht jugendamt fremdgeh seitensprung ehebruch affaere
        affare geliebte
    """,
    "Tod/Trauer": """
        tod tot sterb starb gestorben leiche leichnam sarg grab gruft friedhof beerdig
        begraebnis begrabnis bestatt trauer witwe waise urne hinterblieb nachruf testament
        suizid freitod erhaeng erhang galgen henker hinricht exekut lynch ertrink ertrank
        ertrunken erstick unfall absturz verungl opfer
    """,
    "Gewalt/Waffen/Krieg": """
        mord massaker genozid holocaust gaskammer vergasung gewalt folter quael misshand
        missbrauch schlaeg pruegel prugel ohrfeig waffe gewehr pistol revolver munition patrone
        granat bombe sprengstoff sprengsatz terror attentat anschlag amok krieg soldat schlacht
        panzer messerstech kopfschuss erschies erschoss erstech erstoch erwuerg erwurg wuerg
        gift rache raecher hass feind drohung bedroh erpress entfuehr geisel stalk mobb schikan
        demuetig demutig belaestig uebergriff ubergriff kill explos katastroph tsunami unglueck
        ungluck  kastr
    """,
    "Sexuelles": """
        sex porno erotik erotisch nackt nackig bordell puff hure nutte prostitu 
        zuhaelter zuhalter penis vagina scheide geschlechts beischlaf vorspiel orgasm ejakul
        sperma samenerguss kondom verhuet onanie masturb bums fick poppen geil luestern lustern
        wollust lustmolch busen brust nippel titte arsch hintern pobacke anal fetisch sado maso
        domina schwul lesb homo tunte transe zwitter intim pervers paedo pado kinderschaend
        inzest striptease stripper dirne flittchen schlampe luder schwanz morgenlatte muschi
        pussy fotze kitzler klitoris vorhaut beschneid scham dildo vibrator swinger escort
        callgirl gigolo erektion potenz viagra befriedig verfuehr spanner voyeur exhibitionis
        rammeln kamasutra
    """,
    "Diskriminierung/Beleidigung/Aussehen": """
        neger nigg zigeun kanake kanacke polack kuemmeltuerk schlitzaug mohr eskimo indianer
        rasse rassis nazi hitler fascho faschis hakenkreuz reichsbuerger jude islam moslem
        muslim kopftuch dschihad jihad gastarbeit auslaender auslander fluechtl fluchtl asyl
        abschieb migrant spast mongo idiot depp trottel dumm doof bloed debil schwachsinn
        schwachkopf vollpfost penner asozial gesindel abschaum poebel proll prolet zicke
        miststueck drecksau schwein bastard wichs hurensohn missgeburt spacko dick fett moppel
        pummel wampe kahl zwerg liliput hasenscharte schiel stotter lispel haesslich hasslich
        missgestalt entstellt hexe sekte satan teufel hoelle daemon versager  verlierer
        faulpelz faulenz schmarotz parasit propaganda diktator
    """,
    "Arbeit/Geld": """
        kuendig entlass gefeuert rauswurf rausschmiss abmahn arbeitslos erwerbslos hartz
        buergergeld burgergeld sozialhilfe insolvenz pleite bankrott konkurs schulden verschuld
        pfaendung pfandung armut obdachlos gehalt lohn kurzarbeit stellenabbau personalabbau
        sozialplan abfindung rente streik probezeit befristet kuerzung
    """,
    "Kriminalität": """
        dieb raub einbruch einbrech betrug betrueg falschgeld schmuggel hehler gauner ganove
        verbrech krimin gefaengnis gefangnis knast haeftling haftling haftbefehl haftstraf
        inhaftier verhaft festnahm anklage angeklagt verurteil strafanzeig taeter tater mafia
        korrupt bestech geldwaesch geldwasch dealer straf schuld
    """,
    "Ekel/Ausscheidungen": """
        kot kacke kack scheiss scheis pisse piss pinkel urin furz pups rotz popel schleim
        dreck jauche guelle gulle faekal fakal exkrement
    """,
    "Nachträglich ergänzt": """
        droh erstach ersticht erdrossel qualvoll qualen rentner insolven zickig versag wahn
        vollrausch rauschmittel faulheit rachsucht pulsader tollwut unzucht pocken virolog viren
        toxisch toxik sadist skelett zombie soziopath psychopath endsieg deportation darmentleer
        erfrier erfror halluzin infusion injektion injizier implantat hypochond hysteri paranoi
        letharg morbid makaber nahkampf notwehr peitsch putsch razzia reizgas skalpell tortur
        tyrann umerzieh ungeziefer wurfgeschoss wutanfall wutausbruch zermalm zielscheibe
        zielperson zuckung keuchhust gicht haarausfall hitzschlag kopfweh sodbrenn atemnot asthma
         amnesie agonie delirium deform desorient deprimier exhum fallbeil fieber aderlass
        ableben ehekrise ehedrama eheproblem fehlzeiten fessel gespreizt knebel peinig pubertier
        lasziv liebschaft sinnlich penetrant frivol bestiali bespuck beleidig bewaffn bisswunde
        demotiv denunz detonier dezimier diffamier dilettant ekelhaft eklig eliminier entkleid
        entmutig fahnenflucht fanatiker feigling feigheit fratze gelitten genesen gerippe gesetzlos
        gesoffen gezeugt gutmensch hackbeil haftanstalt haftzeit haftverschon hetzjagd hetzkampagne
        hilflos humpel hyperaktiv illegal infantil inhuman inkubation insasse irrer juckreiz
        kaltgestellt kehlkopf klinisch kollabier kopfgeld korpulent korrumpier krampf kronzeuge
        kurativ langfinger langzeitfolge leibarzt leidtragend leidvoll liquidier lustvoll
        medikament miesmacher militant mollig mundschutz narben neurolog notdurft notleidend
        ohnmacht paranoia pillen poliklin pseudolog querulant rausgeflogen rauswerf resozialis
        sezier sinnkrise sippenhaft soziopath speichel steril stigmatis teuflisch unausstehlich
        undiszipliniert unehrlich ungepflegt unhold unmoralisch unmotiviert unqualifiziert
        unsozial unsympath verachte verklag veruntreu visite vorladung vormund voruntersuch
        wehrlos witzfigur zahnlos zerfetz abnormal abartig abgeurteilt abreibung abserviert
        abspeck abzocke agonie akutmedizin alimente almosen amnesie antibiotik apathisch arrest
        armselig arztbesuch arztpraxen atheis axthieb banditen bazill beinverletzung bettruhe
        blamabel blamier borniert chronisch delinquent ewiggestrig  fallpauschal falschaussag
        geknebel gehemmt gehhilfe gequetscht hautarzt herzrasen hormon schande aussatz
        blind ertaub taubstumm verletz leiden schmerz steif samenbank samenspend besam geburt
        lustgreis lustknab lustobjekt lustschrei lustakt spital tablette brechreiz verhunger
        hungersnot chirurg operation amput dialys diarrh diphther zoster morphin sperm schlamp
        zote sedier devian kerker amnes menorrh gonorrh nekro sklero arthros rheuma migraen
        neuros autis adhs legasthen dyslex inzucht saugakt scharia sklav schubhaft schutzhaft
        kiff
    """,
}

# Regex-Muster, wo ein reiner Teilstring zu viele Fehltreffer hätte
MUSTER = {
    "Diskriminierung/Beleidigung/Aussehen": [r"^loser"],
    "Sexuelles": [r"(^|kuh|schaf|ziegen)euter", r"^freier(n|s)?$"],
    "Gewalt/Waffen/Krieg": [r"(^|ver)elend", r"(?<!ge)wunde(?!r)"],
    "Nachträglich ergänzt": [r"(^|ab|be|an|auf|aus|ge)leck(?!er)", r"^(ge)?oute(n|t|te|ten|st)?$", r"^outing", r"(^|an)ekel", r"(^|ab|an|aus|be|der|er|ver|zu|voll|tot|weg)sauf(?!bau|gab|lauf|guss|nahm|takt|sicht|stieg|trag|wand|wert)"],
    "Psyche/Sucht/Essstörung": [r"(?<![erh])sucht"],
    "Krankheit/Medizin": [r"(?<![pml])pest", r"(^|arzt|krank)attest", r"^niere", r"nierenstein", r"nierenversag", r"nierenkrank", r"spenderniere"],  # nicht: besucht, versucht, Sehnsucht
}

# Harmlose Teilstrings, die vor dem Abgleich aus dem Wort entfernt werden
AUSNAHMEN = """
    kanal analys analyt analog banal analphab marsch barsch harsch archiv gleich bleich
    schleich total totem prototyp toto entscheid unterscheid bescheid granatapfel traub grau
    schraub straub veranstalt spritz kotelett maskott homogen homoop homoeop sprach brach
    drach krach turn pesto method schenk turin taurin purin trotz protz brotz german roman
    osman dominan potenzial potenziell drogerie terrass brasser strasse atemberaub raumord
    unter autot autod foto glimpf haarsch idealer lesbar meerschwein stachelschwein
    wildschwein osterb prassel trasse salzgehalt angehalt ungehalt straff knackt zerbrech
    sehnsucht auspuff boykott damokles fanal beinbruch schimpf drohne belohn lohnen lohnt dickicht puffer
    exekutive mundpropaganda azurn purpurn kothurn burner bourne urner eurin auring euring
    maurin pluder fluder schluder kotext alkotest koteri kotier kokott spiss frotzel frotzl
    harass prass brass krass rassel photo bruttot kontot zytot mitot stotz kustod matod
    astodon schampus schampun schamad schaman schamfil sexam sexport sexpert wegeil album
    sparsch schur androg hydrog drohr eifel geburtstag geburtsort geburtsjahr geburtsdatum
    geburtsname geburtsstadt nautis
"""

def lade_woerter(text):
    return sorted({w for w in text.split() if w}, key=len, reverse=True)

def main():
    eingabe, behalten, entfernt = sys.argv[1:4]
    zusatz = set()
    if len(sys.argv) > 4:
        with open(sys.argv[4], encoding="utf-8") as f:
            zusatz = {z.strip().lower() for z in f if z.strip() and not z.startswith("#")}

    staemme = [(kat, s) for kat, block in STAEMME.items() for s in lade_woerter(block)]
    muster = [(kat, re.compile(m)) for kat, ms in MUSTER.items() for m in ms]
    ausnahmen = lade_woerter(AUSNAHMEN)

    with open(eingabe, encoding="utf-8") as f:
        zeilen = f.read().split("\n")
    if zeilen and zeilen[-1] == "":
        zeilen.pop()

    keep, drop = [], []
    for wort in zeilen:
        w = wort.lower()
        if w in zusatz:
            drop.append(f"{wort}\tmanuell")
            continue
        bereinigt = w
        for a in ausnahmen:
            bereinigt = bereinigt.replace(a, "|")
        grund = next((f"{kat}: {s}" for kat, s in staemme if s in bereinigt), None)
        if grund is None:
            grund = next((f"{kat}: {m.pattern}" for kat, m in muster if m.search(bereinigt)), None)
        (drop.append(f"{wort}\t{grund}") if grund else keep.append(wort))

    with open(behalten, "w", encoding="utf-8") as f:
        f.write("\n".join(keep) + "\n")
    with open(entfernt, "w", encoding="utf-8") as f:
        f.write("\n".join(drop) + "\n")
    print(f"{eingabe}: {len(zeilen)} -> {len(keep)} behalten, {len(drop)} entfernt")

if __name__ == "__main__":
    main()
