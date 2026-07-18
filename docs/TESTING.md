# Testing

Install development dependencies and run:

```bash
python -m pytest
python -m ruff check .
```

The suite covers weighted average cost, invested/current value, unrealized P/L, partial and missing
price coverage, empty portfolios, invalid purchases, SQLite round trips, idempotent demo seeding,
PDF extension/MIME/size/signature/EOF validation, the bundled synthetic PDF, fixture extraction,
mandatory human confirmation, structured OpenAI request construction, and empty parsed responses.
It also covers daily and weekly contributions, prior-week comparison, seven-week baseline,
concentration, allocation shift, best/worst observable day, missing/stale prices, narrative length,
prohibited financial language, deterministic fallback, and guarded generated narratives.

Tests must never call OpenAI, Telegram, yfinance, or any other network service.
