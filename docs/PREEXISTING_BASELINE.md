# Pre-existing baseline

## Provenance

LedgerLens is an extension of a Streamlit investment tracker that existed before the OpenAI
Build Week submission period. The protected source directory was created on June 15, 2026.
The owner states that changes made on July 18, 2026 were dependency and framework maintenance
to mitigate vulnerabilities, not Build Week feature development.

The protected source remains outside this repository and is never modified by the Build Week
project. No real CSV, backup, or invoice was copied or inspected for fixture creation.

Audited source file: `app3prod.py`

SHA-256 after the July 18 maintenance update:

`3324BA920D146B7D3605D6BE02999F93A17FCE151815C245E76E737A8B45D7D1`

This hash identifies the audited maintenance state; it is not presented as a hash captured
before July 13.

## Pre-existing functionality

- Streamlit dashboard for Chilean equities.
- Manual purchase entry.
- Initial and current value calculations.
- Unrealized P/L and portfolio return.
- Weighted average purchase price.
- yfinance market price lookup.
- Local CSV purchase history and backups.
- Basic PDF invoice storage, preview, and download.
- Purchase editing and deletion.
- Portfolio grouping by ticker and platform.

## Not part of the pre-existing baseline

- Modular domain/data/analytics architecture.
- Fully synthetic offline demo mode.
- Fixture market data provider.
- Human-verified OpenAI invoice extraction.
- Daily Lens and Weekly Lens for portfolios.
- Automated tests, privacy checks, Docker, and judge documentation.

## Protected architectural references

Five modules from a separate private production system were inspected in read-only mode only
to understand separation of deterministic KPIs, historical context, AI narrative, fallbacks,
and optional delivery channels. No private names, data, formulas, dependencies, or imports are
copied into LedgerLens.

