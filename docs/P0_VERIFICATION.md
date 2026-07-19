# P0 verification

Verification date: July 18, 2026.

This matrix records executed checks for the mandatory Build Week scope plus the final request-control
and persistent-runtime closure. It does not cover pending Devpost publication, licensing, video
recording, or Session ID collection.

## Functional matrix

| Requirement | Evidence | Result |
| --- | --- | --- |
| Sanitized independent project | Git/privacy scans; protected source remains external | Pass |
| Synthetic dataset and PDF | Bundled fixture portfolio, history, and visually verified PDF | Pass |
| GPT-5.6 invoice extraction | Controlled structured extraction using the synthetic PDF | Pass |
| Editable preview and human confirmation | Browser flow rejected an unchecked save and accepted a reviewed save | Pass |
| Portfolio update | Browser flow changed invested value from 356,000 to 494,000 CLP after confirmation | Pass |
| Daily Analyst | Deterministic KPIs, guarded narrative, missing/stale context tests | Pass |
| Weekly Analyst | Prior week, seven-week baseline, guarded narrative, insufficient baseline test | Pass |
| Request lifecycle | Visible progress, disabled in-flight controls, and duplicate request rejection | Pass |
| Explicit AI Insights | Generate/Refresh action and context/model-bound session cache | Pass |
| Streamlit visibility | Portfolio, import, history, Daily Lens, Weekly Lens, and About rendered | Pass |
| Offline operation | Default app and automated tests require no OpenAI, yfinance, or Telegram access | Pass |
| Automated tests | 67 tests | Pass |
| Reproducible container | Fresh `python:3.13-slim` build and health-checked runtime | Pass |
| Persistent container data | Named volume retained four repository records across two containers | Pass |
| Judge documentation | README, architecture, testing, demo, provenance, changelog, and checklist | Pass |

## Executed verification

- `python -m pytest -q`: 67 passed.
- `python -m ruff check .`: passed.
- `python -m compileall -q app.py ledgerlens sample_data scripts tests`: passed.
- Streamlit AppTest: passed without exceptions; all seven top-level and nested tabs were discovered.
- `docker build --check .`: passed with no warnings.
- `docker build -t ledgerlens:buildweek-ui .`: passed from the current slim base image.
- `docker compose config --quiet`: passed.
- Container health endpoint: HTTP 200 with `ok`.
- Container runtime user: UID 999, not root.
- Container `pip check`: no broken requirements.
- Container contents: synthetic PDF present; `/app/.env` absent.
- Request-control browser check: synthetic PDF extraction showed completion feedback and editable
  review; selecting OpenAI Insights exposed an explicit Generate button without making a request.
- Persistence check: one container wrote four bundled synthetic records through the repository and
  a second container read the same records from the temporary named volume.
- Browser end-to-end flow: upload, extraction preview, confirmation rejection, confirmed save,
  portfolio refresh, Daily Lens, and Weekly Lens passed with no browser-console errors.
- Controlled live GPT-5.6 validation: three HTTP 200 responses; extraction and both narrative
  guardrails passed. Details are in `docs/OPENAI_INTEGRATION.md`.

## Dependency review

Runtime dependencies are explicitly pinned in `requirements.txt`. A fresh Docker installation and
both host/container `pip check` runs completed without conflicts. `docker build --check` reported no
Dockerfile warnings.

An additional `pip-audit` advisory-service query was attempted three times during P0 and once more
during technical closure with a bounded 60-second timeout. The package installed successfully, but
the remote vulnerability service did not return before any timeout, so no CVE result is claimed.
This does not replace the verified dependency consistency checks and should be retried before
public release if the advisory service is available.

## Clean environment

The committed application closure tree at `ddf9653` was exported with `git archive` into a new
temporary directory and installed into a new virtual environment. Before execution, the export
contained no `.git`, `.env`, runtime database, or cache. `pip check`, all 67 tests, Ruff,
compilation, and Streamlit AppTest passed. The temporary environment was then removed.

An earlier isolated export exposed that an unanchored `invoices/` ignore rule had hidden the
`ledgerlens/invoices` source package from Git. The rule was anchored to the root data directory,
the complete package was committed, and a regression test remains in the current 67-test suite.

Status: passed.
