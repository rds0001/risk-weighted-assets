# Risk-Weighted Assets Reference Engine

[![CI](https://github.com/rds0001/risk-weighted-assets/actions/workflows/ci.yml/badge.svg)](https://github.com/rds0001/risk-weighted-assets/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

An institution-neutral, auditable reference implementation for CRR III risk-weighted
assets, capital, IRRBB and ICAAP. The repository combines a Python calculation engine,
canonical Excel contracts, realistic synthetic portfolios, reproducible reference runs,
and a small local web application.

The project is intended for research, education, prototyping and independent model
validation. It is not regulatory, legal, accounting or investment advice, and it is not
a certified reporting system. See [DISCLAIMER.md](DISCLAIMER.md).

## What is included

- CRR III credit risk under SA and IRB, including CRM and output-floor views
- crypto, counterparty credit risk, SFT, CCP, securitisation and CVA modules
- settlement, large exposures, market risk (legacy plus FRTB parallel views) and
  operational risk
- own funds, buffers, leverage, MREL/TLAC and capital headroom
- IRRBB/CSRBB, ICAAP economic and normative perspectives, and double-count controls
- 16 canonical Excel input workbooks and six output workbooks per calculation run
- two synthetic datasets: a broad universal-bank case and a KSA-focused case
- a local browser application that calls the same calculation pipeline as the CLI
- deterministic input/code fingerprints, run manifests, lineage and reconciliation controls

## Quick start

Python 3.10 or newer is required.

```bash
git clone https://github.com/rds0001/risk-weighted-assets.git
cd risk-weighted-assets
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e './code[test]'
./code/rwa run --dataset daten/rechenlaeufe/2026-08-31/v1.0.0
```

Launch the local web interface with:

```bash
./Webapp/rwa-web
```

Then open `http://127.0.0.1:8080`. The server binds to localhost by default.

Generate and calculate a new synthetic dataset:

```bash
./code/rwa all \
  --data-root daten/rechenlaeufe \
  --as-of-date 2026-08-31 \
  --version v1.0.1 \
  --seed 5752026 \
  --bank-profile MID_SIZE_UNIVERSAL
```

## Repository layout

```text
code/        Python engine, command-line interface and automated tests
Webapp/      local browser UI and HTTP layer
daten/       synthetic reference data, configuration and calculation outputs
Standards/   metadata-only inventory of directly linked official sources
docs/        methodology, architecture, operations, governance and source catalogue
tools/       release-integrity and manifest utilities
.github/     continuous-integration workflow
```

No downloaded regulatory PDFs, office documents or other third-party publications are
redistributed. Official links and archival checksums are recorded in
[Standards/00_manifest/sources.json](Standards/00_manifest/sources.json); the broader
research catalogue is in [docs/REGULATORY_SOURCES.md](docs/REGULATORY_SOURCES.md).

## Reproducibility and tests

The two supplied reference datasets use the reporting date 31 August 2026. Each dataset
contains a manifest with SHA-256 hashes and row counts. Its retained reference run has
status `CALCULATED`, six output workbooks and 12 of 12 successful calculation controls.

```bash
python3 -m pytest code/tests
python3 Standards/00_manifest/validate_sources.py
python3 tools/validate_release.py
python3 tools/build_manifest.py --check
```

More detail is available in [docs/CLI_AND_WEBAPP.md](docs/CLI_AND_WEBAPP.md),
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and
[docs/GOVERNANCE_CONTROLS_AND_ACCEPTANCE.md](docs/GOVERNANCE_CONTROLS_AND_ACCEPTANCE.md).

## License and contribution

Copyright © 2026 RiskDataScience GmbH. The repository's original content is licensed
under the [GNU General Public License, version 3 only](LICENSE). External standards and
publications remain subject to their respective rights and are not part of the distribution.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
