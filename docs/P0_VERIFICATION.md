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

## Initial public container verification (superseded)

This section records the initial P0 release. The current multi-broker public release is documented
in the following section.

The public image was built from Git commit `0e33758` with OCI source, revision, title, and MIT
license metadata. Docker Hub exposes `latest`, `buildweek-2026`, and `0e33758` for `linux/amd64`;
all three resolve to manifest digest
`sha256:b5c5f85a5c680cb5d1596855986c25a126e11f8e422add7d748a8300ae2917b7`.

To avoid a cache-only result, all three public-name tags were removed locally while preserving the
independent `ledgerlens:buildweek-ui` backup tag. `alejandroromeroa/ledgerlens:buildweek-2026` was
then pulled from Docker Hub and verified:

- Pulled repository digest matched the published manifest digest.
- OCI revision, source, and MIT license matched the source commit and public GitHub repository.
- Runtime user was UID 999 and `pip check` reported no broken requirements.
- `/app/.env` was absent and the bundled synthetic PDF was present.
- Streamlit AppTest completed with zero exceptions and seven top-level/nested tabs.
- The running health endpoint returned HTTP 200 `ok`.
- A temporary named volume retained four synthetic records across two independent containers.
- The validation container and volume were removed afterward; no user data volume was touched.

No API credential was supplied and no OpenAI, yfinance, Telegram, or application-hosting action
occurred during the public-image validation.

## Multi-broker public container verification (superseded)

The five-invoice release was built from Git commit `4f38f5d` and published as `latest`,
`buildweek-2026`, and immutable tag `4f38f5d`. All three tags resolve to manifest digest
`sha256:d1d2ecd8587847bd15af3c136cbf343cbcaddad01f31154d72bbca31f2964d01` for
`linux/amd64`.

A cache-independent pull of `buildweek-2026` confirmed the expected OCI source revision, five
bundled synthetic PDFs, five catalog entries, non-root runtime user, and absence of `/app/.env`.
Offline extraction returned the matching broker, ticker, amount, and reference for every sample.
Streamlit AppTest completed with zero exceptions, seven tabs, and all five selector options. The
hardened runtime reached healthy state and returned HTTP 200 `ok`.

Docker Scout retained the inherited base-image totals documented in the CVE acknowledgement.
`--only-fixed` and `--ignore-base` both returned zero findings, so the multi-broker application
layer introduced no detected CVEs and no available security update was omitted.

## Auditable-correction public container verification (superseded)

The correction release was built from Git commit `d89a59e` and published as `latest`,
`buildweek-2026`, and immutable tag `d89a59e`. Docker Hub reports manifest digest
`sha256:785085e8c1540dbb2a6125a219b2b1bd2a1c62566bb249ac55efe751411ba513` for all
three tags on `linux/amd64`. A cache-independent pull confirmed the complete OCI source revision.

The candidate was tested against a named volume initialized by the preceding public image. It
additively migrated the existing SQLite schema, atomically voided both active lots for one ticker,
retained all audit records, preserved correction state across a second container and synthetic
seed synchronization, then restored both lots. The temporary labeled volume was removed afterward.

The packaged Streamlit AppTest reported zero exceptions, seven tabs, and the record-management
surface. A hardened runtime reached healthy state, returned HTTP 200 `ok`, and ran as UID 999.
Docker Scout reported the same inherited base-image totals, zero fixable CVEs, and zero CVEs in the
LedgerLens application layer.

## Current branding and Project public container verification

The branded Project release was built from Git commit `89800d2` and published as `latest`,
`buildweek-2026`, and immutable tag `89800d2`. Docker Hub reports manifest digest
`sha256:19d80fdf70625c20d9a28e49e936ad9a9f950bd27d07651ed526f07d797ef6b6` for all
three tags on `linux/amd64`; a cache-independent pull confirmed the complete OCI revision.

The packaged image contains exactly five curated branding PNGs, excludes the original ZIP and
source-pack directory, and contains no `.env`. Streamlit AppTest reported zero exceptions, retained
seven top-level/nested tabs, confirmed Project replaced About, rendered the embedded local header
lockup and four-step workflow, and verified both public links. The hardened runtime returned HTTP
200 `ok` as UID 999.

Docker Scout indexed 197 packages, retained the documented inherited base-image totals, reported
zero fixable CVEs, and reported zero CVEs attributable to the LedgerLens application layer.
