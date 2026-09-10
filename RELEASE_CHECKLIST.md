# Release checklist

Copyright (C) 2026 RiskDataScience GmbH. Licensed under GPL-3.0-only.

- [ ] Confirm copyright ownership and GPL-3.0-only compatibility of every contribution.
- [ ] Confirm that only synthetic data is present and that no secret or personal data exists.
- [ ] Confirm that no downloaded PDF, DOC, DOCX or other third-party publication is bundled.
- [ ] Confirm that internal build-factory and working-material directories are absent.
- [ ] Review all official source URLs and reporting-date qualifications.
- [ ] Run `python3 -m pytest code/tests` successfully.
- [ ] Run `python3 Standards/00_manifest/validate_sources.py` successfully.
- [ ] Run `python3 tools/validate_release.py` successfully.
- [ ] Regenerate `MANIFEST.sha256` with `python3 tools/build_manifest.py`.
- [ ] Run `python3 tools/build_manifest.py --check` successfully.
- [ ] Review `git diff --check`, repository size and executable file modes.
- [ ] Create and push a signed `v1.0.0` tag only after final approval.
