<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/ledgerlens-header-lockup.png">
    <img src="assets/branding/ledgerlens-lockup-navy.png" alt="LedgerLens" width="420">
  </picture>
</p>

<p align="center"><strong>Many sources. One verified view.</strong></p>

# LedgerLens

LedgerLens is an AI-assisted portfolio ledger that turns brokerage invoices into human-verified
purchase records and factual daily and weekly portfolio intelligence. It is designed for retail
investors tracking CLP-denominated Chilean equity portfolios.

This repository is the independent OpenAI Build Week 2026 extension of a pre-existing Streamlit
tracker. The earlier baseline and the new work are separated in
[`docs/PREEXISTING_BASELINE.md`](docs/PREEXISTING_BASELINE.md) and
[`docs/BUILD_WEEK_CHANGELOG.md`](docs/BUILD_WEEK_CHANGELOG.md).

## Official artifacts

- Source repository: [github.com/aguilarbucket/Ledgerlens](https://github.com/aguilarbucket/Ledgerlens)
- Container repository: [alejandroromeroa/ledgerlens](https://hub.docker.com/r/alejandroromeroa/ledgerlens)
- Judge instructions: [`docs/JUDGE_INSTRUCTIONS.md`](docs/JUDGE_INSTRUCTIONS.md)
- Demo video script: [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md)
- Brand system: [`docs/BRANDING.md`](docs/BRANDING.md)

## The problem and solution

Retail investors may hold positions through multiple brokers, each with a separate dashboard.
Brokerage invoices are useful evidence but do not automatically form one trustworthy, explainable
portfolio ledger. LedgerLens validates a PDF, extracts a typed draft, requires a person to review
and confirm every saved record, calculates portfolio metrics deterministically in Python, and then
uses GPT-5.6 only to describe supplied facts.

The complete judge path works offline with fictional data and no external credentials.

```text
synthetic PDF -> validation -> typed extraction -> editable review -> explicit confirmation
              -> SQLite ledger -> deterministic analytics -> Daily Lens / Weekly Lens
```

## Features

- Fully synthetic portfolio, price history, companies, four-broker seed, and five one-page
  brokerage invoices from distinct fictional brokers.
- PDF extension, MIME, size, signature, and EOF validation.
- Offline fixture extraction and optional GPT-5.6 structured extraction through the Responses API.
- Editable preview, field-level confidence, warnings, and mandatory human confirmation.
- SHA-256 document traceability without retaining uploaded PDF bytes.
- Weighted average cost, current value, allocation, price coverage, and unrealized P/L.
- Daily and weekly price contributions, comparable periods, concentration, distribution shift,
  best/worst observable day, missing/stale prices, and context quality.
- Deterministic offline narratives plus optional guarded GPT-5.6 narratives.
- Responsive fintech dashboard with semantic KPI cards, allocation and portfolio-value charts,
  Daily/Weekly contribution visualizations, and explicit data-quality panels.
- Four-step invoice workflow plus auditable purchase-history filters for date, ticker, platform,
  source, and status.
- Reversible record correction can void one erroneous/duplicate purchase or every active lot for a
  ticker without erasing history; voided records are excluded from portfolio calculations.
- Visible multi-step request progress, per-session in-flight locking, and explicit AI Insight
  generation so Streamlit reruns cannot silently create duplicate model requests.
- Local SQLite persistence backed by an optional named Docker volume, automated tests, and a
  reproducible container image.

## Architecture

Financial truth and generated language are deliberately separated:

- `ledgerlens/domain`: typed purchase and market records.
- `ledgerlens/data`: SQLite persistence and synthetic seed synchronization.
- `ledgerlens/market`: fixture and optional yfinance providers.
- `ledgerlens/analytics`: deterministic financial and historical calculations.
- `ledgerlens/invoices`: PDF validation, extraction schemas, and confirmation rules.
- `ledgerlens/ai`: one centralized Responses API client; no financial calculations.
- `ledgerlens/analysts`: Daily/Weekly narrative orchestration and guardrails.
- `ledgerlens/ui`: offline design tokens, accessible components, chart specifications, and
  Streamlit views; it reshapes calculated values but never recalculates financial metrics.
- `app.py`: Streamlit composition and human review workflow.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for calculation and persistence boundaries.
The implemented visual system and verification evidence are in
[`docs/UI_IMPLEMENTATION.md`](docs/UI_IMPLEMENTATION.md).

## Run locally

Python 3.11 or newer is required. Python 3.13 is used by the Docker image.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

Open `http://localhost:8501`. The default creates an ignored database at
`runtime/ledgerlens.db`. All displayed records and market prices are fictional.

## Run with Docker

No API key is needed for the reproducible judge path.

### Published image

The following commands work unchanged in Windows PowerShell, Command Prompt, Bash, and zsh:

```console
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run --rm --name ledgerlens -p 127.0.0.1:8501:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 alejandroromeroa/ledgerlens:buildweek-2026
```

Open `http://localhost:8501`. Add `--env-file .env` before the image name only when testing the
live OpenAI path. The named
`ledgerlens-data` volume retains confirmed purchases when the container is stopped, removed, or
rebuilt. Uploaded PDFs, unconfirmed drafts, and API credentials are not stored in that volume.

### Build the image locally

```console
docker build -t ledgerlens:buildweek-ui .
docker run --rm --name ledgerlens-local -p 127.0.0.1:8501:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 ledgerlens:buildweek-ui
```

Docker Compose provides the same persistent setup and automatically reads the ignored local
`.env` file when it exists:

```bash
docker compose up --build
docker compose down
```

Do not use `docker compose down --volumes` unless the confirmed-purchase database should be
deleted. The container runs as an unprivileged user, includes a health check, and excludes local
credentials, databases, logs, private PDFs, CSV files, and virtual environments from its build
context.

## Environment variables

Copy `.env.example` to the ignored `.env` only when live OpenAI features are required.

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | unset | Optional live Responses API authentication. |
| `OPENAI_MODEL` | `gpt-5.6` | Exact model used for live extraction and narratives. |
| `LEDGERLENS_DEMO_MODE` | `true` | Keeps this Build Week slice on synthetic data. |
| `LEDGERLENS_DATABASE_PATH` | `runtime/ledgerlens.db` | Local SQLite database location. |
| `LEDGERLENS_MAX_PDF_MB` | `10` | Maximum accepted upload size. |

Missing credentials never block the offline demo. Live invoice extraction fails explicitly;
Daily and Weekly Lens show a clearly labeled deterministic fallback. LedgerLens never silently
switches to another model.

## Test and verification

```bash
python -m pytest
python -m ruff check .
python -m compileall -q app.py ledgerlens sample_data scripts tests
```

The optional live smoke test is billable, uses only bundled synthetic inputs, disables automatic
SDK retries, and makes at most three API attempts:

```bash
python -m scripts.validate_openai_live --confirm-live
```

See [`docs/TESTING.md`](docs/TESTING.md) and
[`docs/P0_VERIFICATION.md`](docs/P0_VERIFICATION.md) for the verified matrix and exact boundaries.

## Five-minute judge path

1. Start the app without an API key and confirm the synthetic-data banner.
2. In **Import purchase**, choose one of five bundled synthetic invoices, download it, and upload
   it back to LedgerLens.
3. Use **Offline fixture**, validate the PDF, and inspect the editable typed preview.
4. Show that saving is rejected until the explicit confirmation checkbox is selected.
5. Confirm the record and inspect the updated dashboard, filtered ledger, and truncated document
   hash.
6. Show allocation, observable value, position cards, and the detailed-table fallback.
7. Open **Daily Lens** and **Weekly Lens** and compare contribution charts, context quality,
   deterministic KPIs, and narrative source labels.
8. Optionally explain the already-validated GPT-5.6 path; judges do not need a credential.

The concise recording sequence is in [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md).
Exact clean-machine commands and expected results are in
[`docs/JUDGE_INSTRUCTIONS.md`](docs/JUDGE_INSTRUCTIONS.md).

## GPT-5.6 and human control

LedgerLens uses GPT-5.6 through the official Responses API for two bounded tasks: extracting a
strict invoice draft and writing short descriptions of Python-calculated KPI contexts. Requests
use `store=False`. The model does not calculate portfolio values, decide what to save, infer
missing money values, recommend trades, predict prices, or invent causes.

A human must review and confirm an extraction before it becomes a purchase. The uploaded PDF is
processed in memory and is not persisted.

## Privacy and security

- Only synthetic data belongs in the repository, tests, screenshots, and demo.
- `.gitignore` and `.dockerignore` exclude credentials, runtime databases, invoices, CSV files,
  backups, logs, caches, and temporary data.
- No private system is imported or required; Telegram is absent from the P0 runtime.
- API keys are read only from the process environment or ignored local `.env` and are never logged.
- No repository remote, publication, deployment, or external service connection is required.
- The current public-image scan, inherited Debian CVEs, compensating controls, and time-bounded demo
  acceptance are documented in
  [`docs/SECURITY_CVE_ACKNOWLEDGEMENT.md`](docs/SECURITY_CVE_ACKNOWLEDGEMENT.md).

## Limitations

- Purchases are supported; sales, realized gains, tax accounting, and closed-position returns are
  not implemented.
- The public demo uses synthetic CLP prices and is not a source of live market truth.
- yfinance is an optional adapter and is not used by the offline app or tests.
- There is no multi-user authentication, banking integration, trading automation, price forecast,
  portfolio optimization, news feed, or personalized advice.

## Codex collaboration and human decisions

Codex was used in the primary project session to audit the baseline, design the modular extension,
implement and test the Build Week work, validate the GPT-5.6 integration, and prepare judge-facing
documentation. The human owner established provenance, confirmed that July 18 baseline work was
security/framework maintenance, selected the product scope, authorized the independent sanitized
directory, controlled the API credential and usage limit, and retains authority over publication,
licensing, deployment, and submission.

## Financial disclaimer

LedgerLens is descriptive demonstration software, not financial, investment, tax, or legal advice.
All portfolio values and entities in the demo are fictional. Reported P/L is unrealized because the
current product records purchases, not sales.

## License

LedgerLens is released under the [MIT License](LICENSE).
