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
