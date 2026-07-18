# Architecture

LedgerLens separates financial truth from generated narrative.

1. Domain models represent confirmed purchases, market prices, and calculated metrics.
2. Repository adapters own persistence and can be replaced without changing analytics.
3. Market providers return timestamped prices; fixture mode is the reproducible default.
4. Analytics calculates all monetary values, returns, allocation, and data quality in Python.
5. Invoice validation checks extension, MIME type, size, PDF signature, and EOF before extraction.
6. Invoice extractors return a strict Pydantic model with field-level confidence and warnings.
7. The centralized OpenAI client uses an in-memory Base64 PDF input, `store=False`, structured
   parsing, configurable model/timeout, and metadata-only logging.
8. Streamlit owns editable preview state; the repository rejects any workflow that has not passed
   explicit human confirmation.
9. Analyst modules receive structured deterministic context and may only produce narrative.

Historical intelligence uses timestamped fixture prices and confirmed purchases to construct
comparable snapshots. Market movement excludes the cash effect of purchases made inside the
comparison period; those purchases are reported separately. Daily and weekly narratives consume
serialized KPI contexts and pass through word-count and financial-language guardrails.

SQLite is used locally for traceability and transactional writes. Runtime databases are ignored
by Git. Confirmed invoice purchases retain the source, confirmation timestamp, document reference,
and SHA-256; uploaded bytes are not persisted. The repository contains synthetic fixtures only.
