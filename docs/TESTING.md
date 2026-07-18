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

## Controlled live OpenAI validation

After configuring an ignored local `.env`, run the opt-in smoke check:

```bash
python -m scripts.validate_openai_live --confirm-live
```

The command makes exactly three requests using only bundled synthetic data: one structured PDF
extraction plus one guarded Daily Lens and one guarded Weekly Lens narrative. It reports model,
latency, and pass/fail status without printing the API key, document body, prompts, or narratives.
Automatic SDK retries are disabled for this validator so transient failures cannot exceed the
three-attempt ceiling.
