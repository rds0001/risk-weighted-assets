# RWA Control Center

Die Web-App ist eine additive, lokale Bedienoberfläche für die bestehende RWA
Engine. Sie verändert weder Rechenkern noch Excel-Datenverträge. Ein Klick auf
„Gesamtlauf starten“ ruft unverändert `rwa_engine.pipeline.run_dataset()` für
das ausgewählte versionierte Datensatzverzeichnis auf.

## Start

```bash
./Webapp/rwa-web
```

Danach im Browser öffnen:

```text
http://127.0.0.1:8080
```

Abweichende Datenwurzel oder Port:

```bash
./Webapp/rwa-web --data-root daten/rechenlaeufe --host 127.0.0.1 --port 8081
```

Der Standard bindet ausschließlich an den lokalen Rechner. Für einen Betrieb
im Netzwerk sind davor Authentisierung, TLS, Reverse Proxy, Rollenmodell und
Betriebsfreigabe einzurichten.

## Funktionsumfang

- Auswahl aus `daten/rechenlaeufe/YYYY-MM-DD/version`
- Anzeige von Stichtag, Version, Bankprofil, Tabellen und Inputzeilen
- Vollständigkeitsstatus und Download aller 16 Input-Workbooks
- Auswahl historischer Rechenläufe
- Anzeige zentraler RWA-, Kapital-, IRRBB- und ICAAP-Kennzahlen
- Kontrollstatus und Download sämtlicher Output-Workbooks
- idempotenter Gesamtlauf mit Schutz gegen parallele Doppelstarts je Datensatz
- kontrollierte Fehlermeldungen für abgelehnte Läufe

Die Oberfläche ändert oder lädt keine Excel-Dateien hoch. Reale Daten werden
weiterhin kontrolliert in den versionierten Input-Workbooks gepflegt. Nach dem
Speichern genügt „Aktualisieren“ und anschließend „Gesamtlauf starten“.

## Technik und Sicherheit

Die App nutzt ausschließlich Python-Standardbibliothek plus die bereits
installierte RWA Engine. Dateidownloads sind auf bekannte Datensatzpfade und
`.xlsx`-Dateien begrenzt; Pfadtraversierung wird abgewiesen. Es werden keine
Geschäfts- oder Regelwerte in der Web-Schicht gehalten.
