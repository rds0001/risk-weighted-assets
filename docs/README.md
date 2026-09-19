# Documentation map

Version 1.2.0: [SME/infrastructure supporting factors, eligibility inputs and audit outputs](SUPPORTING_FACTORS.md).

Copyright (C) 2026 RiskDataScience GmbH. Licensed under GPL-3.0-only.

The documentation is organized so that management scope, regulatory methodology,
implementation details and operating evidence can be reviewed independently.

## Orientation and scope

- [Management and scope](MANAGEMENT_AND_SCOPE.md): objectives, supported views,
  boundaries and end-to-end processing.
- [Architecture](ARCHITECTURE.md): components, dependencies, repository layout and
  implemented calculation modules.
- [Disclaimer](../DISCLAIMER.md): limitations and mandatory preconditions for production use.

## Regulatory and quantitative methodology

- [Pillar 1 methodology](PILLAR_1_METHODOLOGY.md): SA/IRB credit risk, CRM, CCR/SFT/CCP,
  securitisation, CVA, settlement, market and operational risk, own funds and output floor.
- [Pillar 2, IRRBB and ICAAP methodology](PILLAR_2_IRRBB_ICAAP.md): EVE/NII, CSRBB,
  economic-capital aggregation, normative projections and RWA equivalents.
- [Regulatory source catalogue](REGULATORY_SOURCES.md): reporting-date qualifications
  and official links. Referenced publications are external and are not redistributed.
- [Sources and intellectual property](SOURCES_AND_INTELLECTUAL_PROPERTY.md): provenance,
  checksums, synthetic-data boundary and third-party rights.

## Data, operation and verification

- [Data model and history](DATA_MODEL_AND_HISTORY.md): canonical entities, temporal axes,
  keys, lineage, versioning and mandatory controls.
- [Excel data household](EXCEL_DATA_HOUSEHOLD.md): all 16 input and six output workbooks,
  shared contracts and editing rules.
- [CLI and web application](CLI_AND_WEBAPP.md): commands, local UI, functions and security.
- [Installation and troubleshooting](INSTALLATION_AND_TROUBLESHOOTING.md): environment,
  diagnosis, backup and recovery.
- [Reference profiles and testing](REFERENCE_PROFILES_AND_TESTING.md): supplied synthetic
  cases, expected evidence and verification procedure.
- [Governance, controls and acceptance](GOVERNANCE_CONTROLS_AND_ACCEPTANCE.md): change
  governance, test pyramid, release gates and remaining institution-specific sign-offs.
- [Glossary and appendix](GLOSSARY_AND_APPENDIX.md): terms, key metrics and reproducibility
  commands.

The German methodology is the detailed technical/fachlich reference supplied with version
1.0.0. Root-level English documents define the public repository, license and contribution
boundary.
