# 10. Installation, Betriebsvoraussetzungen und Troubleshooting

## Voraussetzungen

- Linux-/WSL- oder vergleichbare Python-Umgebung.
- Python ab Version 3.10.
- pandas, NumPy, openpyxl, PyYAML und SciPy in kompatiblen Versionen.
- Schreibrechte im Projekt, insbesondere unter `daten/rechenlaeufe`.
- Browser mit aktiviertem JavaScript für die Web-App.

Die bereitgestellten Launcher setzen `PYTHONNOUSERSITE=1`, damit inkompatible
Pakete aus einem Benutzerpfad die geprüfte Systemumgebung nicht überlagern.
Sie setzen außerdem den Python-Suchpfad relativ zum Repository; ein globales
Installieren des Projekts ist für den lokalen Betrieb nicht erforderlich.

## Erstprüfung

```bash
git clone https://github.com/rds0001/risk-weighted-assets.git
cd risk-weighted-assets
./code/rwa --help
./Webapp/rwa-web --help
cd code
PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest
```

Erwartet werden 44 bestandene Tests. HTTP-Integrationstests benötigen die
Erlaubnis, einen lokalen Loopback-Socket zu öffnen.

## Typische Fehlerbilder

### `ModuleNotFoundError`

Immer die Launcher `./code/rwa` beziehungsweise `./Webapp/rwa-web` verwenden.
Bei direktem Python-Aufruf müssen `code` und für die Web-App zusätzlich
`Webapp` im `PYTHONPATH` stehen.

### Port bereits belegt

```bash
./Webapp/rwa-web --port 8081
```

Dann `http://127.0.0.1:8081` öffnen. Alternativ den bereits laufenden lokalen
Prozess kontrolliert beenden.

### Browser zeigt keine Verbindung

- Prüfen, ob das Terminal weiterhin den Webserver ausführt.
- Angezeigte Adresse und Port exakt übernehmen.
- `http://`, nicht `https://`, für den lokalen Standard verwenden.
- Health Check aufrufen: `http://127.0.0.1:8080/api/health`.

### Datensatz fehlt in der Auswahl

Der Pfad muss exakt `daten/rechenlaeufe/YYYY-MM-DD/version/inputs` enthalten.
Das Datum muss ISO-Format haben; der Versionsname darf Buchstaben, Zahlen,
Punkt, Unterstrich und Bindestrich enthalten.

### Lauf wird `REJECTED`

Das erzeugte `*_REJECTED.xlsx` öffnen und `Validation_Issues` bearbeiten.
Häufige Ursachen sind fehlende Workbooks/Sheets/Spalten, ungültige
Wertebereiche, doppelte Official-Datensätze, gebrochene Referenzen, fehlende
Parameter oder ein nicht passender SHA-256-Hash einer Rechtsquelle.

### Input wird als „Bearbeitet“ angezeigt

Die Datei unterscheidet sich vom Erzeugungsmanifest. Das ist nach bewusster
fachlicher Bearbeitung erwartbar. Stichtag und Version prüfen und niemals eine
freigegebene alte Version überschreiben. Der neue Lauf erhält automatisch
einen neuen Inputhash und Fingerprint.

### Excel-Datei gesperrt oder nicht schreibbar

Excel-Datei schließen, Dateirechte prüfen und sicherstellen, dass der
Outputordner beschreibbar ist. Inputs werden beim reinen `run` nicht verändert;
`all` materialisiert das ausgewählte Referenzprofil neu.

### Lange Laufzeit

Ein neuer Fingerprint führt sämtliche Berechnungen und Excel-Exporte aus.
Ein identischer, bereits erfolgreich berechneter Fingerprint wird idempotent
wiederverwendet. Während eines Laufs den Browser nicht mehrfach starten;
parallele Doppelstarts desselben Datensatzes werden mit HTTP 409 abgewiesen.

### NumPy-/pandas-Binärfehler

Den bereitgestellten Launcher verwenden. Keine Pakete ungeprüft in die
Systemumgebung installieren. Benötigte Versionsänderungen zuerst in einer
separaten Umgebung testen und danach die vollständige Suite ausführen.

## Backup und Recovery

Vor produktiver Nutzung sind regelmäßige, unveränderbare Backups von
`daten/`, `Regularien/`, `code/` und `Webapp/` vorzusehen. Zur Reproduktion
eines Laufs werden Input-Workbooks, Regelkonfiguration, lokale Rechtsquellen,
Codeversion und Run-Manifest benötigt. Wiederherstellung ist durch erneuten
Lauf und Vergleich des Calculation Fingerprint zu testen.
