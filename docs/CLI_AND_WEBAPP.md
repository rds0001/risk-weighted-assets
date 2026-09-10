# 9. Bedienung der CLI und Browser-App

## Browser-App exakt starten

1. Terminal öffnen.
2. In das Projektverzeichnis wechseln:

```bash
git clone https://github.com/rds0001/risk-weighted-assets.git
cd risk-weighted-assets
```

3. Web-App starten:

```bash
./Webapp/rwa-web
```

4. Die Ausgabe muss `RWA Web App: http://127.0.0.1:8080` und den Datenpfad
   `.../daten/rechenlaeufe` zeigen.
5. Browser öffnen und exakt folgende Adresse eingeben:

```text
http://127.0.0.1:8080
```

6. In „Stichtag und Datenversion“ den gewünschten Datensatz auswählen.
7. Input-Vollständigkeit und Bearbeitungsstatus prüfen.
8. „Gesamtlauf starten“ wählen und bis zur Erfolgsmeldung warten.
9. Kennzahlen und Kontrollstatus prüfen; anschließend die gewünschten
   Output-Workbooks herunterladen.
10. Server im Terminal mit `Ctrl+C` sauber beenden.

## Sichtbare Informationen

Die Kopfleiste zeigt Backend-Verfügbarkeit. Metakarten zeigen Stichtag,
Datenversion, Bankprofil, Anzahl der Fachtabellen und Inputzeilen. Die
Inputtabelle zeigt pro Workbook Umfang, Größe, Manifeststatus und Download.
Ergebniskarten zeigen TREA, CET1- und Gesamtkapitalquote, Output Floor,
EVE-/NII-SOT, ökonomischen Headroom sowie bestandene Kontrollen und
Validierungsbefunde. Historische Läufe bleiben auswählbar.

## CLI-Bedienung

```bash
# Bestehenden Datensatz rechnen
./code/rwa run --dataset daten/rechenlaeufe/2026-08-31/v1.0.0

# Referenzprofil erzeugen und vollständig rechnen
./code/rwa all --bank-profile MID_SIZE_UNIVERSAL

# KSA-Profil erzeugen und vollständig rechnen
./code/rwa all --bank-profile KSA_BANK --version v1.0.0-ksa

# Leere Templates erzeugen
./code/rwa templates --output daten/templates/v1.0.0
```

## Abweichender Port oder Datenpfad

```bash
./Webapp/rwa-web --host 127.0.0.1 --port 8081
./Webapp/rwa-web --data-root /absoluter/pfad/zu/rechenlaeufen
```

Bei Port `8081` lautet die Browseradresse `http://127.0.0.1:8081`. Die Bindung
an `0.0.0.0` ist ohne Authentisierung, TLS und Firewallfreigabe nicht zulässig.

## Vollständige Web-App-Funktionsbeschreibung

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
