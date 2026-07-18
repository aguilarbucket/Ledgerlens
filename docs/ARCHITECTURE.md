# Architecture

LedgerLens separates financial truth from generated narrative.

1. Domain models represent confirmed purchases, market prices, and calculated metrics.
2. Repository adapters own persistence and can be replaced without changing analytics.
3. Market providers return timestamped prices; fixture mode is the reproducible default.
4. Analytics calculates all monetary values, returns, allocation, and data quality in Python.
5. AI modules will receive structured deterministic context and may only produce narrative.
6. Streamlit composes these modules and owns human confirmation states.

SQLite is used locally for traceability and transactional writes. Runtime databases are ignored
by Git. The repository contains synthetic Python fixtures only.

