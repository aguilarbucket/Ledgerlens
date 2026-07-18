# Testing

Install development dependencies and run:

```bash
python -m pytest
python -m ruff check .
```

The initial suite covers weighted average cost, invested/current value, unrealized P/L, partial
and missing price coverage, empty portfolios, invalid purchases, SQLite round trips, and
idempotent demo seeding.

Tests must never call OpenAI, Telegram, yfinance, or any other network service.

