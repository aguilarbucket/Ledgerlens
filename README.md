# LedgerLens

LedgerLens is an AI-assisted portfolio ledger that turns brokerage invoices into human-verified
purchase records and factual portfolio intelligence. The initial audience is retail investors
tracking CLP-denominated equity portfolios.

This repository is the OpenAI Build Week extension of a pre-existing Streamlit tracker. Only
work added for Build Week is evaluated here; the baseline is documented in
`docs/PREEXISTING_BASELINE.md`.

## Current vertical slice

The first slice is fully offline and synthetic:

`synthetic purchases -> fixture prices -> deterministic metrics -> Streamlit portfolio`

It demonstrates weighted average cost, current value, unrealized P/L, allocation, missing-price
handling, and price coverage without external credentials.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

The default demo creates a local ignored database under `runtime/`. All displayed data is
fictional.

## Test

```bash
python -m pytest
python -m ruff check .
```

## Environment

Copy `.env.example` to `.env` only when live integrations are ready. Never commit `.env`.
`OPENAI_API_KEY` is not required for the current slice.

## Privacy and financial boundaries

- No real portfolio, invoice, account, Telegram identifier, or private-system export belongs in
  this repository.
- AI will not calculate financial metrics, choose saved records, predict prices, or recommend
  buying, selling, or holding.
- LedgerLens currently records purchases only. It reports unrealized P/L, not realized gains.
- Generated analysis is descriptive and is not financial advice.

## Planned Build Week flow

1. Upload a fully synthetic brokerage PDF.
2. Extract typed fields with GPT-5.6 through the Responses API.
3. Review and edit the preview.
4. Save only after explicit human confirmation.
5. Recalculate the portfolio deterministically.
6. Generate factual Daily Lens and Weekly Lens narratives from structured Python context.

## Codex collaboration

Codex is being used in the main project session to audit the baseline, design the architecture,
implement and test the extension, and prepare privacy and judge documentation. The human owner
defines product scope, confirms provenance, controls credentials, and authorizes any future
publication or deployment.

