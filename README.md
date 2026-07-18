# LedgerLens

LedgerLens is an AI-assisted portfolio ledger that turns brokerage invoices into human-verified
purchase records and factual portfolio intelligence. The initial audience is retail investors
tracking CLP-denominated equity portfolios.

This repository is the OpenAI Build Week extension of a pre-existing Streamlit tracker. Only
work added for Build Week is evaluated here; the baseline is documented in
`docs/PREEXISTING_BASELINE.md`.

## Current product flow

The implemented flow is fully usable without credentials:

`synthetic PDF -> validation -> structured fixture extraction -> editable preview -> explicit
confirmation -> deterministic portfolio`

The fixture extraction is clearly labeled and makes no model request. If `OPENAI_API_KEY` is
configured, the same validated PDF and typed response model can be sent through the official
Responses API. The uploaded PDF is processed in memory and is not persisted; LedgerLens retains
only its SHA-256 with the confirmed purchase for traceability.

Portfolio analytics demonstrate weighted average cost, current value, unrealized P/L, allocation,
missing-price handling, and price coverage without external credentials.

Daily Lens and Weekly Lens are also implemented from a synthetic historical price series. Python
calculates price contributions, comparable-period movement, concentration, distribution shift,
best/worst observable day, additions, invoice completeness, stale prices, and context quality.
Both reports have a deterministic offline narrative and an optional guarded OpenAI narrative.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

The default demo creates a local ignored database under `runtime/`. All displayed data is
fictional. A polished synthetic PDF is available at
`output/pdf/ledgerlens_synthetic_invoice.pdf`.

## Test

```bash
python -m pytest
python -m ruff check .
```

The optional live smoke check is explicitly billable and uses only the bundled synthetic data:

```bash
python -m scripts.validate_openai_live --confirm-live
```

## Environment

Copy `.env.example` to `.env` only when live integrations are ready. Never commit `.env`.
`OPENAI_API_KEY` is not required for fixture extraction. Selecting OpenAI mode without a key fails
explicitly and never silently falls back to another model or saves a purchase.

## Privacy and financial boundaries

- No real portfolio, invoice, account, Telegram identifier, or private-system export belongs in
  this repository.
- AI will not calculate financial metrics, choose saved records, predict prices, or recommend
  buying, selling, or holding.
- LedgerLens currently records purchases only. It reports unrealized P/L, not realized gains.
- Generated analysis is descriptive and is not financial advice.

## Planned Build Week flow

1. Upload a fully synthetic brokerage PDF. **Implemented.**
2. Extract typed fields using a fixture or GPT-5.6 through the Responses API. **Implemented and
   validated live with the synthetic PDF.**
3. Review and edit the preview. **Implemented.**
4. Save only after explicit human confirmation. **Implemented.**
5. Recalculate the portfolio deterministically. **Implemented.**
6. Generate factual Daily Lens and Weekly Lens narratives. **Implemented with offline fallback and
   validated live through their financial-language guardrails.**

## Codex collaboration

Codex is being used in the main project session to audit the baseline, design the architecture,
implement and test the extension, and prepare privacy and judge documentation. The human owner
defines product scope, confirms provenance, controls credentials, and authorizes any future
publication or deployment.
