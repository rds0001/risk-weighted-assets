# External regulatory sources

Copyright (C) 2026 RiskDataScience GmbH. Licensed under GPL-3.0-only.

This directory deliberately contains source metadata only. No regulatory PDF, guideline,
standard or other third-party publication is redistributed with the software.

`00_manifest/sources.json` is the machine-readable provenance boundary for the two legal
sources referenced directly from the supplied Excel datasets. It records official URLs and
the SHA-256 values of the copies used during development. The checksum is evidential: a
publisher may later replace a file at the same URL. The broader, human-readable research
catalogue is maintained in `docs/REGULATORY_SOURCES.md`.

Validate the boundary offline with:

```bash
python3 Standards/00_manifest/validate_sources.py
```

Users are responsible for obtaining applicable source documents from their official
publishers and verifying currency, authenticity, legal status and redistribution terms.
