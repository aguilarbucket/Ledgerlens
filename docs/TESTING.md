# Testing

Install development dependencies and run:

```bash
python -m pytest
python -m ruff check .
python -m compileall -q app.py ledgerlens sample_data scripts tests
```

The suite covers weighted average cost, invested/current value, unrealized P/L, partial and missing
price coverage, empty portfolios, invalid purchases, SQLite round trips, idempotent demo seeding,
PDF extension/MIME/size/signature/EOF validation, the bundled synthetic PDF, fixture extraction,
mandatory human confirmation, structured OpenAI request construction, and empty parsed responses.
It also covers daily and weekly contributions, prior-week comparison, seven-week baseline,
concentration, allocation shift, best/worst observable day, missing/stale prices, narrative length,
prohibited financial language, deterministic fallback, and guarded generated narratives.
It also verifies missing credentials, absence of Telegram from the runtime, fixture-only demo
market data, root-anchored private invoice exclusions, and Docker credential boundaries.
The UI suite additionally covers escaped component content, semantic movement labels, stable chart
colors, deterministic view-model reshaping, portfolio history, platform allocation, workflow
states, confidence visualization, and composable read-only history filters.

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

## P0 reproducibility checks

The final P0 matrix also builds Docker from the current slim base, checks the health endpoint,
confirms an unprivileged runtime user, verifies `.env` is absent from the image, and exercises the
complete synthetic invoice workflow in a browser. A committed-tree export is installed into a new
virtual environment without Git metadata, `.env`, runtime databases, or caches. See
`docs/P0_VERIFICATION.md` for executed results and the dependency-audit note.

## Fintech UI verification

The completed UI pass contains 65 automated tests. Streamlit AppTest discovers the five expected
Altair charts and all seven top-level/nested tabs. Browser checks cover 390, 768, and 1280 px,
mandatory confirmation, confirmed portfolio refresh, and absence of error-level console messages.
A fresh image build is healthy at `/_stcore/health`, runs as UID 999, and renders the dashboard.
See `docs/UI_IMPLEMENTATION.md` for the executed matrix.
