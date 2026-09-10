# 7. Aufbau des Programms, Komponenten und Libraries

## Architekturüberblick

Die Anwendung ist modular, dateibasiert und lokal ausführbar. Der Rechenkern
unter `code/rwa_engine` kennt Fachalgorithmen, Datenverträge, Validierung,
Parameterzugriff und Orchestrierung. Die Web-App unter `Webapp/rwa_web` ist
eine additive HTTP-Schicht und ruft unverändert `run_dataset()` auf. Die
Excel-Dateien bleiben der führende Ein- und Ausgabekanal.

```text
Browser
  → lokaler Python-HTTP-Server
    → Datensatzkatalog und sichere Downloads
    → bestehende run_dataset-Pipeline
      → Excel-Import und Validierung
      → Fachengines und Aggregationen
      → Excel-Export, Audit und Manifest
```

## Python-Komponenten

| Komponente | Verantwortung |
|---|---|
| `config_io.py` | YAML-Profile, Regelsätze und Parametermatrizen laden |
| `contracts.py` | kanonische Tabellen-, Spalten- und Schlüsselverträge |
| `excel_io.py` | Excel-Import/-Export, Templates und Validierung |
| `parameters.py` | fail-closed Zugriff auf externe regulatorische Parameter |
| `formulas.py` | atomare, möglichst pure Rechenfunktionen |
| `engines.py` | risikomodulweise Berechnung und Aggregation |
| `pipeline.py` | End-to-End-Orchestrierung, Fingerprints, Outputs und Audit |
| `synthetic.py` | Integritätsprüfung und Materialisierung externer Profile |
| `cli.py` | Kommandozeilenschnittstelle |
| `rwa_web/catalog.py` | Datensatz-, Lauf- und Dateikatalog |
| `rwa_web/server.py` | lokale HTTP-API und Run-Button |

## Verwendete Libraries

- Python 3.10 oder höher als Laufzeit.
- pandas 2.2.2 für tabellarische Verarbeitung und Excel-Integration.
- NumPy 1.26.4 für Vektor-, Matrix- und Korrelationsrechnungen.
- openpyxl als Excel-Engine und für strukturierte Workbooks.
- PyYAML für externe Regelsatz- und Profilkonfiguration.
- `statistics.NormalDist` aus der Python-Standardbibliothek für Verteilungsfunktionen.
- pytest und Hypothesis ausschließlich für Tests.
- Python-Standardbibliothek `http.server` für die lokale Browser-App.

Es wurden für die Web-App keine zusätzlichen Pakete installiert. Die lokale
Bindung an `127.0.0.1` vermeidet eine unbeabsichtigte Netzfreigabe. Für einen
Mehrbenutzerbetrieb sind Reverse Proxy, TLS, Authentisierung und
Rollenberechtigungen vorgeschaltet bereitzustellen.

## Aktuelle Verzeichnisstruktur

```text
code/                         Python-Rechenkern, CLI und Tests
Webapp/                       lokales Browser-Frontend und Python-Web-Backend
daten/
├── rechenlaeufe/             versionierte Excel-Inputs und -Outputs
├── referenzprofile/          versiegelte synthetische Ausgangsdaten
└── konfiguration/            Bankprofile und regulatorische YAML-Parameter
Standards/                    Metadaten zu externen amtlichen Quellen
docs/                         Methodik, Betrieb, Governance und Quellenkatalog
tools/                        reproduzierbare Release- und Integritätsprüfungen
```

## Einstiegspunkte

```bash
./code/rwa --help
./Webapp/rwa-web
cd code && PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest
```

Code und Web-App lösen ihre Pfade relativ zum Repository auf. Die Befehle
funktionieren daher auch, wenn sie aus einem anderen Arbeitsverzeichnis
aufgerufen werden.

## Operationalisierter Implementierungsstand

**Version:** 1.0.0  
**Referenzstichtag:** 31.08.2026

**Daten-/Regeltrennung:** Geschäfts-, Markt-, Szenario-, Generator- und
Regelwerte liegen ausschließlich in versionierten YAML-/Excel-Datenquellen.
Der Python-Code enthält nur Rechenalgorithmen, Schema, Validierung und
Orchestrierung. Referenzprofile und Rechenläufe sind per SHA-256 nachvollziehbar.

| Bereich | Implementiert | Atomarer Output | Parallel-/Kontrollsicht |
|---|---:|---|---|
| KSA EAD/CCF/RW | ja | `SA_Detail` | KSA-Shadow für S-TREA |
| Immobilien/ETV/Loan Splitting | ja | Segmente in `SA_Detail` | Pre-/Post-CRM |
| CRM/Substitution | ja | Schutzbetrag und Substitutions-RW | Allokationsprüfung |
| IRB Corporate/Retail/Floors/EL | ja | `IRB_Detail` | Shortfall/Excess |
| Crypto-Übergang | ja | `Crypto_Detail` | Tier-1-Limitkennzeichen |
| SA-CCR/SFT | ja | `CCR_Detail`, `SFT_Detail` | S-TREA |
| CCP | ja | `CCP_Detail` | QCCP/NQCCP |
| Verbriefung | ja | `SEC_Detail` | exakte SSFA-Grenztranche, SEC-IRBA/SA/ERBA, STS/NPE/Resec |
| CVA | ja | `CVA_Summary`, `CVA_Buckets` | BA-CVA mit Hedge-Mismatch und SA-CVA parallel |
| Settlement/Free Delivery | ja | `Settlement_Detail` | – |
| Großkreditüberschreitung | ja | `Large_Exposure` | – |
| Markt Legacy | ja | `Market_Legacy` | offizieller 2026-Ansatz |
| FRTB-SA | ja | `FRTB_Buckets`, `FRTB_Risk_Classes`, `FRTB_DRC`, `FRTB_Summary` | drei Korrelationsszenarien, DRC und RRAO; fully-loaded |
| FRTB-IMA | ja | `FRTB_IMA` | Yesterday/60-Tage IMCC/SES, PLA, DRC/Add-ons; genehmigungsabhängig |
| Operationelles Risiko BIC | ja | `Operational_Risk` | ILM-Kontrolle |
| U-/S-TREA und Output Floor | ja | `TREA_Summary` | `Floor_Allocation` |
| AVA/NPE-Backstop | ja | `Prudent_Valuation`, `NPE_Backstop` | CET1-Abzug |
| CET1/AT1/T2 | ja | `Capital_Stack` | explizite Abzüge/Amortisation |
| P2R/Puffer/P2G | ja | `Capital_Stack` | Kapitalqualitäten |
| Leverage/MREL/TLAC | ja | `Parallel_Constraints` | getrennte Restriktionen |
| IRRBB EVE/sechs Schocks/SOT | ja | `IRRBB_Scenarios`, `IRRBB_Currency_Scenarios` | Mehrwährung, VaR/ES |
| NII/EaR/NII-SOT | ja | `IRRBB_Repricing_Gap`, `IRRBB_NII_Bands`, `IRRBB_Scenarios` | periodisch/Constant Balance |
| CSRBB | ja | `IRRBB_Risk_Measures` | Stressverlust |
| ICAAP Economic Capital | ja | `EC_Standalone`, `EC_Aggregation` | Korrelation/Diversifikation |
| ICAAP normative Perspektive | ja | `Normative_Projection` | Base/Adverse |
| P2R-/EC-/IRRBB-RWA-Äquivalent | ja | `RWA_Equivalents`, `Pillar2_Bridge` | Double-Count-Control |
| Bitemporal/Official | ja | Audit/Run-Metadaten | Official-Designation |
| Lineage/Reconciliation | ja | Audit-Workbook | Formelregister/Input-, Code- und Lauf-Fingerprint |

Die Tabelle bezeichnet die operationalisierte Rechenschicht, nicht automatisch
die fachliche Produktivfreigabe jeder CRR-Sonderkonstellation. Der genaue
Abnahmeumfang und die institutsbezogenen Freigabepunkte stehen in
`docs/GOVERNANCE_CONTROLS_AND_ACCEPTANCE.md`. Instituts- oder rechtsstandsabhängige Parameter
bleiben versionierte Eingabedaten und müssen vor einem offiziellen Einsatz
freigegeben werden.

Der aktuelle externe Regelkatalog umfasst 418 materialisierte Parameterzeilen.
Die automatisierte Testsuite umfasst 44 Tests; die beiden Referenzprofile
erreichen jeweils 12 von 12 Laufkontrollen ohne Validierungsfehler.
