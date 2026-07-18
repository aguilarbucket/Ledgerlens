# LedgerLens contributor guide

## Architecture

- `ledgerlens/domain`: typed financial records.
- `ledgerlens/data`: persistence adapters.
- `ledgerlens/market`: live and synthetic market data providers.
- `ledgerlens/analytics`: deterministic calculations only.
- `ledgerlens/invoices`: PDF validation, typed extraction records, and confirmation rules.
- `ledgerlens/ai`: OpenAI integration; never performs financial calculations.
- `ledgerlens/analysts`: daily and weekly narrative orchestration.
- `app.py`: Streamlit composition layer.

## Commands

- Install: `python -m pip install -r requirements-dev.txt`
- Run: `streamlit run app.py`
- Test: `python -m pytest`
- Lint: `python -m ruff check .`

## Non-negotiable rules

- Use only synthetic data in the repository, tests, screenshots, and demo.
- Never commit `.env`, API keys, invoices, local databases, portfolio exports, or logs.
- Financial metrics are calculated deterministically in Python.
- AI text is descriptive only: no advice, predictions, invented causes, or trade actions.
- Use “unrealized P/L”; the current product records purchases, not sales.
- Saving an extracted invoice requires explicit human confirmation.
- The application and tests must work without OpenAI, Telegram, yfinance, or internet access.

## Definition of Done

A change is done when its deterministic behavior is tested, offline demo behavior still works,
privacy boundaries are preserved, documentation is updated, and lint/tests pass.
