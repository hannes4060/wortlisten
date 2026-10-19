# Deutsche Wortlisten für KeePassXC
[KeePassXC](https://keepassxc.org/) kann neben zufällig gewürfelten Passwörtern auch aus Wortlisten zufällige Passphrasen erzeugen. Diese haben den Vorteil, dass man sie sich deutlich leichter merken kann. Leider hat [KeePassXC](https://github.com/keepassxreboot/keepassxc) nach der Installation nur eine englische Wortliste auf Lager. Für alle, die gerne Deutsche Passphrasen würfeln möchten, hier zwei Listen deutscher Wörter, die man dafür nutzen kann. Einfach nach dem Download der Liste in dem entsprechenden Fenster in KeePassXC zur Passphrasenerzeugungn hinter der englischen Liste auf das Plus-Symbol klicken und die neue Liste auswählen. Schwupps: Schon kann man deutschsprachige Passphrasen erzeugen.

## german_words.geprueft.wordlist
Empfohlen für Passphrasen, die an Mitarbeitende gehen. Die Liste hat 7.586 Einträge: die bereinigte Shortlist und die bereinigte Kinderliste zusammengeführt (kleingeschrieben, ohne Doppelte). Jedes Wort darin wurde einzeln auf heikle oder zweideutige Bedeutungen geprüft. Mit 5 Wörtern ergeben sich rund 64 Bit Entropie.

## german_words.wordlist
Diese Liste hat 336.898 Einträge und wurde u.a. aus folgenden Quellen erstellt:
- https://github.com/enz/german-wordlist
- https://github.com/davidblitz/german-wordlist
- https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4

Zudem wurden alle Wörter mit weniger als vier oder mehr als 10 Buchstaben entfernt. Auch Wörter mit ä, ö, ü oder ß wurden ausgefiltert.

## german_words.shortlist.wordlist
Diese Liste hat nur 7.262 Einträge und besteht nur aus wenigen Wörtern in Grundform, die man sich deutlich leichter merken kann. Dafür ist die [Entropie](https://specopssoft.com/de/blog/alles-ueber-passwort-entropie/) des Passworts nicht so gut.

Die Liste ist ein leicht modifizierte Form dieser Quelle: https://github.com/dys2p/wordlists-de

## german_words.basics_kids.wordlist
538 Wörter aus einem [Wortschatz für Grundschüler](https://bildungsserver.berlin-brandenburg.de/fileadmin/bbb/unterricht/faecher/sprachen/deutsch/Grundschule/Grundwortschatz_BB_WEB_2013.pdf). Alle Wörter <4 und >10 Zeichen wurden entfernt, und ä/ö/ü wurde durch ae/oe/ue ersetzt.
Offensichtlich geringe Entropie, aber ein Einstieg, wenn man jüngeren Kindern direkt sinnvolle Passwörter beibringen möchte ;-)

## Bereinigung heikler Wörter
Aus allen drei Listen wurden Wörter entfernt, die in einem generierten Passwort unangenehm wirken könnten, z. B. weil sie Krankheit, Tod, Gewalt, Sexuelles, Beleidigungen, Diskriminierung, Sucht, Kriminalität oder Kündigung/Geld berühren (Beispiel: Ein Passwort wie „Krebstherapie2026!“ soll nicht entstehen).

- Die Shortlist und die Kinderliste wurden zusätzlich Wort für Wort durchgesehen.
- Die große Liste wurde über Wortstämme gefiltert und stichprobenartig geprüft. Einzelne Ausreißer sind dort weiterhin möglich.
- Das Skript und die Stammliste liegen in `filter/`. Erneut anwenden: `python3 filter/filter.py <eingabe> <behalten> <entfernt> filter/manuell.txt`. Weitere Einzelwörter lassen sich in `filter/manuell.txt` ergänzen.
