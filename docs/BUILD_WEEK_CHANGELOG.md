# Build Week changelog

## 2026-07-18 — Project start

### Codex contributions

- Audited the protected baseline and recorded its maintenance-state SHA-256.
- Identified and preserved privacy boundaries around real purchases, invoices, backups, and
  private production modules.
- Created a clean, independent LedgerLens project.
- Added typed domain records, SQLite persistence, a fixture market provider, deterministic
  portfolio metrics, synthetic demo data, and an initial Streamlit portfolio view.
- Added initial automated tests and contributor rules.

### Human decisions

- The owner confirmed that July 18 changes to the original application were security-driven
  dependency/framework maintenance and not Build Week feature work.
- The owner authorized an independent project directory and deferred API key creation until a
  controlled integration test is required.

### Validation

- Clean virtual environment created with Python 3.13.11.
- Declared runtime and development dependencies installed successfully. The installation command
  reached its execution timeout after packages were installed; package versions were then
  verified directly inside the virtual environment.
- `python -m pytest`: 7 tests passed.
- `python -m ruff check .`: all checks passed.
- Python bytecode compilation: passed.
- Streamlit in-memory smoke test: passed with Portfolio, Purchase history, and About tabs.
- Privacy scan: no personal paths, private-system names, Telegram identifiers, or API key values
  found in project files.
- No OpenAI, Telegram, or yfinance calls were made.

## 2026-07-18 — Human-verified invoice import

### Codex contributions

- Added strict PDF validation for extension, MIME type, configurable size, signature, and EOF.
- Added typed invoice extraction with per-field confidence and warnings.
- Added a centralized Responses API client using in-memory Base64 PDF input, `store=False`,
  configurable model/timeout, and metadata-only logging.
- Added explicit offline fixture and OpenAI extraction modes; no silent fallback occurs.
- Added an editable Streamlit preview and mandatory confirmation before repository writes.
- Added SHA-256 traceability without persisting uploaded PDF bytes.
- Generated and visually verified a one-page synthetic brokerage invoice.

### Validation

- Official OpenAI file-input documentation was checked for Base64 `input_file` request shape.
- Installed SDK signature was inspected for `responses.parse` and typed `text_format` support.
- Automated tests: 17 passed.
- Ruff, compilation, and Streamlit smoke test passed.
- No real OpenAI request was made and no API key was configured.

## 2026-07-18 — Daily Lens and Weekly Lens

### Codex contributions

- Added a reproducible synthetic price history spanning the current week, prior week, and seven
  observable baseline weeks.
- Added deterministic portfolio snapshots and comparable-period price contribution calculations.
- Added Daily Lens KPIs for portfolio value, observable daily movement, unrealized P/L, ticker
  contributions, concentration, new purchases/invoices, price coverage, missing/stale prices, and
  context quality.
- Added Weekly Lens KPIs for prior-week difference, baseline average, ticker contributions,
  concentration/distribution changes, best/worst observable day, positions added, invoice gaps,
  incomplete records, coverage, and context quality.
- Added offline factual narratives and optional OpenAI narratives with word-count, advisory,
  prediction, and invented-causality guardrails.
- Added Streamlit Daily Lens and Weekly Lens views; no Telegram dependency is required.

### Validation

- `python -m pytest`: 25 tests passed.
- `python -m ruff check .`: all checks passed.
- Python compilation and Streamlit in-memory smoke test passed.
- No OpenAI, Telegram, or yfinance request was made.

## 2026-07-18 — Controlled live OpenAI validation

### Codex contributions

- Added project-local `.env` loading that preserves explicit process environment values.
- Added an opt-in validator capped at three billable requests and restricted to bundled synthetic
  inputs.
- Recorded only model, latency, and pass/fail metadata; no credential, prompt, document body, or
  generated narrative was printed or persisted.

### Human decisions

- The owner created the limited-use API credential locally and confirmed readiness for the
  controlled test.

### Validation

- `gpt-5.6` structured synthetic PDF extraction: passed, 5.835 seconds.
- `gpt-5.6` Daily Lens narrative guardrails: passed, 4.087 seconds.
- `gpt-5.6` Weekly Lens narrative guardrails: passed, 4.888 seconds.
- Exactly three Responses API requests completed with HTTP 200; `store=False` remained enforced.
- `python -m pytest`: 27 tests passed.
- `python -m ruff check .`: all checks passed.

## 2026-07-18 — P0 closure

### Codex contributions

- Added a root-scoped `.dockerignore` so local credentials and runtime data cannot enter the image
  while application source packages remain available.
- Hardened Docker with an unprivileged runtime user, explicit synthetic configuration, and a
  health check.
- Added missing-key, insufficient-context, dependency-boundary, and ignore-rule regression tests.
- Expanded the English README with architecture, judge quickstart, environment, limitations,
  privacy, GPT-5.6, Codex collaboration, human decisions, and financial disclaimer sections.
- Added an executed P0 verification matrix.

### Validation

- Initial clean-tree export correctly failed because the generic `invoices/` ignore rule had hidden
  the `ledgerlens/invoices` source package from Git.
- Anchored the private-data exclusion to `/invoices/`, committed the complete invoice package, and
  added a regression test.
- Repeated the clean export into a new virtual environment with no Git metadata, `.env`, database,
  or cache: `pip check`, 34 tests, Ruff, compilation, and Streamlit AppTest passed.
- Fresh Docker build and final rebuild passed; the container was healthy, returned HTTP 200, ran as
  UID 999, imported the invoice package, included the synthetic PDF, and contained no `.env`.
- Browser workflow passed upload, preview, unchecked-save rejection, confirmed save, portfolio
  refresh, Daily Lens, and Weekly Lens with no console errors.
- Final tracked-file scans found no API key patterns, personal paths, or private-system names.
- External `pip-audit` advisory queries timed out; no CVE result is claimed. Host/container
  dependency consistency passed with pinned requirements and `pip check`.

## 2026-07-18 — Fintech UI/UX implementation

### Codex contributions

- Added an offline fintech design system with semantic financial colors, responsive layouts,
  reduced-motion support, visible focus treatment, and reusable escaped components.
- Redesigned Portfolio with KPI cards, current allocation, observable value history, compact
  position cards, platform distribution, and a detailed table fallback.
- Redesigned Daily and Weekly Lens with deterministic contribution charts, weekly baseline
  comparison, narrative panels, context quality, and explicit positive/negative text.
- Added a four-step invoice workflow, source and confidence presentation, privacy explanation,
  two-column review, and preserved mandatory confirmation.
- Added read-only purchase-history filters and visible-record summaries without edit or delete
  operations.
- Added dedicated analytics for historical portfolio values and platform allocation so financial
  calculations remain outside the UI layer.

### Validation

- `python -m pytest`: 65 tests passed.
- `python -m ruff check .` and Python compilation passed.
- Streamlit AppTest passed with five Altair charts and seven top-level/nested tabs.
- Browser checks passed at 390, 768, and 1280 px with no global horizontal overflow.
- The unchecked invoice save was rejected; confirmed save updated invested value from 356,000 to
  494,000 CLP and retained only the document SHA-256.
- Browser logs contained no errors; Vega emitted transient warnings during hidden-tab rerenders.
- Fresh Docker image built successfully, returned HTTP 200 `ok`, ran as UID 999, and rendered the
  portfolio dashboard.
- No OpenAI, yfinance, Telegram, remote Git, deployment, or publication action occurred.

## 2026-07-18 — Request control and persistent Docker runtime

### Codex contributions

- Added per-session idle, pending, and running request states with duplicate in-flight rejection.
- Added visible staged progress and completion/error feedback to invoice extraction.
- Replaced automatic OpenAI narrative generation on Streamlit reruns with an explicit Generate or
  Refresh action.
- Added session-only Daily/Weekly narrative caching keyed by deterministic context and model.
- Added a named Docker volume configuration that preserves confirmed SQLite purchases across
  container replacement without persisting uploaded PDFs, drafts, or credentials.
- Added Docker Compose and updated judge-facing Docker commands.

### Human decisions

- The owner requested visible loading feedback so users cannot start another request while the
  first response is pending.
- The owner requested persistence for confirmed changes across container runs while preserving the
  existing privacy and human-confirmation boundaries.

### Validation

- `python -m pytest`: 67 tests passed.
- `python -m ruff check .` and Python compilation passed.
- Streamlit AppTest completed without exceptions.
- Browser validation loaded and extracted the bundled synthetic PDF through the offline path;
  completion feedback and the editable review rendered correctly.
- Selecting OpenAI narrative mode exposed an explicit Generate action and did not make a request.
- A temporary named volume retained four synthetic repository records across two independent
  containers and was removed after verification.
- `ledgerlens:buildweek-ui` rebuilt successfully and its health endpoint returned HTTP 200.
- A final bounded `pip-audit` retry timed out without an advisory response; no CVE result is
  claimed, while host, clean-environment, and container `pip check` remained clean.
- No live OpenAI, yfinance, Telegram, deployment, remote push, or publication action occurred in
  this closure validation.

## 2026-07-18 — Submission licensing

### Human decision

- The owner delegated the public repository license choice for the hackathon submission.
- MIT was selected to provide a short, widely recognized permission grant suitable for public
  judging, testing, modification, and redistribution.

### Codex contribution

- Added the canonical MIT license with attribution to LedgerLens contributors.
- Linked the license from the README and recorded it in the submission checklist.

### Boundary

- No Git remote was configured and no repository or container image was published in this step.

## 2026-07-18 — Public artifact and judge-instruction preparation

### Human decision

- The owner selected `aguilarbucket/Ledgerlens` as the public source repository and
  `alejandroromeroa/ledgerlens` as the public Docker Hub repository.

### Codex contribution

- Added canonical GitHub and Docker Hub links to the README.
- Added exact public-image pull/run commands while retaining a local-build path.
- Added clean-machine judge instructions with container, source-build, port-conflict, persistence,
  walkthrough, and expected-boundary guidance.

### Boundary

- The destination URLs were verified as public. The GitHub repository remains empty and the Docker
  image pull remains pending until the separate publication phase; no remote, push, or deployment
  action occurred here.

## 2026-07-18 — Public GitHub publication

### Human decision

- The owner explicitly authorized proceeding with the public GitHub publication phase using
  `aguilarbucket/Ledgerlens`.

### Publication

- Configured `origin` as `https://github.com/aguilarbucket/Ledgerlens.git`.
- Published the complete dated `main` history without force-push or history rewriting.
- Verified that local and remote `main` resolved to commit `2112304` immediately after the initial
  push.
- The repository is public and includes the MIT license, synthetic fixtures, reproducible Docker
  configuration, judge instructions, provenance, tests, and privacy boundaries.

### Boundary

- No Docker Hub image was pushed and no application hosting or external deployment occurred in
  this phase.

## 2026-07-18 — Public Docker Hub publication

### Human decision

- The owner explicitly authorized publishing the release image to
  `alejandroromeroa/ledgerlens` after the public GitHub validation.

### Publication

- Added OCI title, description, source, MIT license, and exact Git revision metadata.
- Built from Git commit `0e33758` using the current `python:3.13-slim` base.
- Published `latest`, `buildweek-2026`, and immutable commit tag `0e33758`.
- Docker Hub reported a single `linux/amd64` manifest digest for all three tags:
  `sha256:b5c5f85a5c680cb5d1596855986c25a126e11f8e422add7d748a8300ae2917b7`.

### Public pull validation

- Removed the three public-name tags locally while retaining an independent local backup tag, then
  pulled `alejandroromeroa/ledgerlens:buildweek-2026` from Docker Hub.
- Confirmed the pulled digest, OCI revision/source/license, UID 999, dependency consistency,
  synthetic PDF presence, and `.env` absence.
- Streamlit AppTest returned zero exceptions and seven top-level/nested tabs; container health was
  HTTP 200 `ok`.
- A temporary volume retained four synthetic repository records across two independent containers
  and was removed with the validation container.

### Boundary

- No API key was supplied, no live OpenAI/yfinance/Telegram request occurred, and no hosted
  application deployment was created.

## 2026-07-19 — Cross-shell Docker quickstart correction

### User validation

- The owner successfully pulled the public `buildweek-2026` image and confirmed the published
  manifest digest.
- The multiline Bash example failed in Windows PowerShell because PowerShell does not use `\` as
  its line-continuation character.

### Documentation correction

- Replaced multiline `docker run` examples with quoted, single-line commands that work unchanged
  in Windows PowerShell, Command Prompt, Bash, and zsh.
- Updated the README, judge instructions, and Devpost submission copy without changing or
  rebuilding the verified container image.
- Added a version-controlled Docker Hub description containing the same cross-platform quickstart
  and direct links to the public source and judge documentation.

## 2026-07-19 — CVE acknowledgement and runtime hardening

### Scan evidence

- Docker Scout reported `1 critical`, `2 high`, `3 medium`, `25 low`, and `7 unspecified`
  findings, with identical totals attributed to the official `python:3.13-slim` base.
- The critical and high findings were all inherited through essential Debian
  `perl-base 5.40.1-6`; the refreshed Debian Trixie repositories offered no newer candidate.
- `docker scout cves --only-fixed` and `docker scout cves --ignore-base` both reported zero CVEs.
- Python dependency consistency remained clean with `pip check`.

### Decision and mitigation

- The owner rejected an Alpine migration for the Build Week demo and authorized a transparent,
  time-bounded CVE risk acknowledgement.
- Added a public acknowledgement with the affected CVEs, exposure assessment, patch status,
  review triggers, and remediation plan.
- Hardened Docker Compose and every judge quickstart with localhost-only binding, a read-only root
  filesystem, isolated `noexec`/`nosuid` tmpfs, all capabilities dropped,
  `no-new-privileges`, and CPU, memory, and PID limits.

### Validation

- The unchanged public image became healthy under all compensating controls, returned HTTP 200
  `ok`, and continued to run as UID 999.
- The effective runtime reported read-only rootfs, `CapDrop=ALL`,
  `no-new-privileges:true`, 256 PIDs, 1 GiB memory, 2 CPUs, and loopback-only port binding.
- Temporary Alpine, hardened-validation, and volume resources were stopped or removed; no image
  was published and no API key or private data was used.

## 2026-07-19 — Multi-broker demo and video preparation

### Human decisions

- The owner confirmed registration and participation in OpenAI Build Week on Devpost.
- The owner requested five compatible synthetic invoices covering different brokers, tickers,
  dates, quantities, and amounts.
- The public video remains the primary pending deliverable; the majority-work `/feedback` Session
  ID will be captured last.

### Codex contributions

- Replaced the single hard-coded invoice fixture with a typed five-invoice synthetic catalog.
- Updated fixture extraction to return the fields belonging to each bundled sample filename and to
  reject unknown filenames instead of silently returning unrelated fields.
- Added a five-option invoice selector to Streamlit and distributed the initial portfolio across
  four fictional brokers so the multi-broker use case is visible.
- Prepared a 2:45 English demo script covering the problem, working product, GPT-5.6 integration,
  Codex collaboration, human decisions, and recording-safety checklist.

### Validation

- Generated five distinct one-page A4 PDFs and verified their broker, ticker, transaction fields,
  document references, and synthetic disclaimers through PDF text extraction.
- Rendered all five PDFs to PNG and visually verified typography, alignment, table layout,
  monetary formatting, legibility, and absence of clipping or overlap.
- The expanded suite passed 78 tests; Ruff and bytecode compilation passed.
- Streamlit AppTest returned zero exceptions, seven tabs, one sample selector, and five options.

### Boundary

- No OpenAI request was made, no API key or private data was exposed, no video was uploaded, and no
  `/feedback` Session ID was captured in this phase.

### Public release

- Published the multi-broker application from commit `4f38f5d` as Docker tags `latest`,
  `buildweek-2026`, and immutable tag `4f38f5d`.
- All current release tags resolve to manifest digest
  `sha256:d1d2ecd8587847bd15af3c136cbf343cbcaddad01f31154d72bbca31f2964d01`.
- A cache-independent pull confirmed the OCI revision, five bundled invoices, five catalog
  entries, non-root runtime, absence of `.env`, successful offline extraction, healthy HTTP
  response, and zero Streamlit AppTest exceptions.
- Docker Scout reconfirmed that the application layer introduces no detected CVEs and that no
  fixed CVEs are currently available for the inherited base-image findings.

### Session reference

- The owner supplied and confirmed the majority-work Codex Session ID:
  `019f774d-149c-78e2-b363-28a6ba9205f9`.
- The Devpost draft and submission checklist now include the reference. The public video remains
  the only intentionally pending submission field.
