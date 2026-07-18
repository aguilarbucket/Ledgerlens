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

