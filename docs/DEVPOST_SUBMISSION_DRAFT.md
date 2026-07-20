# Devpost submission draft

Status: owner-approved submission copy. Only the public video URL remains intentionally blank.

## Project name

LedgerLens

## Tagline

Turn brokerage PDFs into human-verified portfolio records and factual AI-assisted intelligence.

## Category

Apps for Your Life — Personal Finance

## Public links

- Source code: https://github.com/aguilarbucket/Ledgerlens
- Container image: https://hub.docker.com/r/alejandroromeroa/ledgerlens
- Stable judge image: `alejandroromeroa/ledgerlens:buildweek-2026`
- License: MIT

## Short description

LedgerLens is an AI-assisted portfolio ledger for retail investors tracking Chilean equities in
CLP. It converts a brokerage invoice into a typed, editable purchase draft, requires explicit human
confirmation, updates a persistent portfolio ledger, calculates financial metrics deterministically
in Python, and presents factual Daily and Weekly portfolio intelligence. GPT-5.6 is used only for
structured invoice extraction and guarded narrative generation; it never calculates portfolio
values, decides what to save, recommends trades, predicts prices, or invents market causes. The
public judge path uses fully synthetic data and runs without credentials or internet-dependent
market data.

## Inspiration

As an amateur investor, I manage investments through more than one brokerage. Each broker presents
the portfolio through a different dashboard, which makes it difficult to maintain a simple,
unified view of positions and purchase history. More advanced platforms such as TradingView can be
valuable, but they can also feel overwhelming when the immediate need is simply to consolidate and
track personal investments clearly.

Brokerage invoices are evidence of a transaction, but they do not automatically become a
trustworthy, explainable portfolio history. Manual transcription creates friction and errors, while
generic AI summaries can blur the line between extracted facts, calculated metrics, and financial
advice. LedgerLens was designed around a stricter boundary: AI can help interpret a document and
communicate supplied facts, but a person confirms the record and deterministic code owns the
financial truth. LedgerLens began by simplifying a problem that was useful for my own portfolio
tracking. If that simpler, unified workflow helps me, it may also help other individual investors
who face the same fragmentation across brokers.

## What it does

1. Accepts a brokerage invoice PDF and validates its extension, MIME type, size, signature, and
   end-of-file marker.
2. Uses GPT-5.6 through the OpenAI Responses API to return a typed draft containing company,
   ticker, quantity, unit price, date, platform, currency, document reference, confidence, and
   warnings.
3. Displays an editable preview and refuses to save until the user explicitly confirms review.
4. Stores the confirmed purchase and document SHA-256 in SQLite without retaining the uploaded PDF.
5. Allows an erroneous or duplicate record, or every active lot for a ticker, to be voided with an
   audit reason and restored without representing the correction as a sale.
6. Calculates invested value, current value, allocation, price coverage, and unrealized P/L in
   Python.
7. Produces Daily Lens and Weekly Lens contexts covering observable movement, ticker contribution,
   concentration, data coverage, missing or stale prices, prior periods, and historical baseline.
8. Optionally asks GPT-5.6 to write short factual narratives from those precomputed contexts.
9. Falls back to deterministic local narratives when credentials, network access, model output, or
   guardrail validation is unavailable.

The interface also exposes progress states and disables in-flight controls so an ordinary
Streamlit rerun or repeated click cannot silently create duplicate model requests. Confirmed
purchases survive container replacement through a named Docker volume; credentials, PDFs,
unconfirmed drafts, and session-cached narratives do not.

## How we built it

LedgerLens uses Streamlit for the product interface, Pydantic for typed extraction contracts,
SQLite for confirmed portfolio records, Altair for deterministic visualizations, and the official
OpenAI Python SDK with the Responses API. The codebase separates domain models, persistence,
market providers, analytics, invoice validation, OpenAI integration, analyst orchestration, and UI
composition.

All financial calculations remain in deterministic Python modules. The OpenAI client is
centralized, reads `OPENAI_API_KEY` only from the environment, uses a configurable `OPENAI_MODEL`
with `gpt-5.6` as the Build Week default, sends the synthetic PDF in memory, requests structured
output, sets `store=False`, applies timeouts, and logs only model, latency, and status metadata.

The public demo includes synthetic purchases across four fictional brokers, fictional companies,
fixture price history, and five generated one-page brokerage invoices. It is packaged as an
unprivileged, health-checked Docker
image and can run without OpenAI, yfinance, Telegram, or any private system.

## How Codex was used

Codex was the primary engineering collaborator for the Build Week extension. It audited the
protected baseline in read-only mode, established privacy boundaries, proposed the modular
architecture, implemented the synthetic vertical slice, built the typed PDF workflow, integrated
the Responses API, developed the Daily and Weekly analysts, created the fintech UI system, added
request locking and Docker persistence, generated tests and documentation, and repeatedly validated
clean exports, browser behavior, containers, public GitHub contents, and the public Docker image.

Codex accelerated implementation, refactoring, testing, and release verification. The human owner
made the material product and governance decisions: selecting the personal-finance problem,
confirming baseline provenance, requiring a separate sanitized repository, approving the
human-confirmation model, controlling API credentials and spend, selecting the UI direction,
choosing the publication destinations, and authorizing licensing and public release.

## How GPT-5.6 was used

GPT-5.6 performs two bounded tasks:

- Structured extraction of necessary fields from a validated synthetic brokerage PDF.
- Short Daily and Weekly descriptions generated only from deterministic KPI contexts supplied by
  Python.

Generated narratives must satisfy word limits and language guardrails that reject advice,
predictions, invented causality, and realized-gain claims. Failed or unavailable responses produce
a clearly labeled deterministic fallback. A controlled live validation completed one structured
PDF extraction and two guarded narrative requests successfully using only bundled synthetic data.
The public offline path does not require judges to provide an API key.

## Existing project versus Build Week work

A Streamlit investment tracker existed before the submission period. Its baseline included a
dashboard, manual purchase entry, CSV history, yfinance lookup, weighted-average calculations,
unrealized P/L, basic invoice storage, and purchase editing or deletion.

The Build Week extension created the independent LedgerLens repository and added the modular
domain/data/analytics architecture, synthetic offline demo, fixture market provider, typed
GPT-5.6 invoice extraction, strict in-memory PDF validation, editable human confirmation, SHA-256
traceability, SQLite repository, Daily Lens, Weekly Lens, deterministic narrative fallback,
financial-language guardrails, fintech interface, automated tests, Docker release, public judge
instructions, and provenance documentation. Only the work added during the submission period is
presented as Build Week work.

## Challenges

- Preserving a useful pre-existing concept without copying private data, production dependencies,
  or business-specific behavior.
- Keeping AI assistance separate from deterministic financial calculations and save authority.
- Designing a demo that remains complete and reproducible without credentials or live market data.
- Preventing normal Streamlit reruns from creating repeated billable narrative requests.
- Making confirmed records persistent across ephemeral containers without persisting sensitive
  uploads or credentials.
- Producing auditable evidence from clean environments, browser flows, public source, and a public
  container registry.

## Accomplishments

- End-to-end synthetic invoice flow with typed extraction, editable review, mandatory confirmation,
  persistent ledger update, and document-hash traceability.
- Deterministic Daily and Weekly portfolio intelligence with guarded optional GPT-5.6 narratives.
- Offline-first fintech interface with semantic financial colors, responsive charts, source labels,
  confidence, context quality, and readable positive/negative states.
- 89 automated tests plus lint, compilation, Streamlit AppTest, browser, clean-export, Docker,
  privacy, and persistence validation.
- Public MIT-licensed GitHub repository and versioned `linux/amd64` Docker image running as an
  unprivileged user.

## What we learned

AI is more trustworthy in a financial workflow when its authority is deliberately narrow. Typed
outputs, explicit human confirmation, deterministic calculation, visible source labels, and local
fallbacks are product features, not just implementation details. Reproducibility also changes the
design: synthetic data, fixture providers, bounded model calls, and containerized execution made it
possible to demonstrate the complete workflow without exposing a real portfolio or requiring judge
credentials.

## What's next

Potential future work includes report export, optional bilingual presentation, configurable
benchmarks, and stronger data-quality alerts. Sales, realized gains, tax accounting, authentication,
bank integrations, automated trading, recommendations, and price predictions remain intentionally
outside the current scope.

## Built with

- Codex
- GPT-5.6
- OpenAI Responses API
- Python 3.13
- Streamlit
- Pydantic
- SQLite
- Altair
- Docker
- pytest
- Ruff

## Judge quickstart

The following commands work unchanged in Windows PowerShell, Command Prompt, Bash, and zsh. Host
port 8502 avoids collisions with the usual local Streamlit port 8501:

```console
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run -d --rm --name ledgerlens -p 127.0.0.1:8502:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 alejandroromeroa/ledgerlens:buildweek-2026
```

Open `http://localhost:8502`, choose one of five bundled synthetic invoices, use Offline fixture
extraction, confirm the purchase, and inspect Portfolio, Purchase history, Daily Lens, and Weekly
Lens. Stop it with `docker stop ledgerlens`. If port 8502 is occupied, inspect it with
`docker ps --filter publish=8502` or use host port 8503. Full troubleshooting is in
`docs/JUDGE_INSTRUCTIONS.md`.

## Verified release references

- Public application source revision: `a154858`
- Current release tags: `latest`, `buildweek-2026`, `a154858`
- Public image platform: `linux/amd64`
- Public image manifest digest:
  `sha256:890e87740ff4372082ef34d0f26565f5f79b13c7b7485d1439093d98a77846d1`
- Verified public source revision:
  `a1548583e96390c45a59c991cb9392454c34a0a9`

## Pending submission fields

- Public YouTube video URL: `[PENDING]`
- Majority-work Codex Session ID from `/feedback`:
  `019f774d-149c-78e2-b363-28a6ba9205f9`
- Owner approval of this English submission copy: approved on 2026-07-19.
