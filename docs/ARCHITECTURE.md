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
10. Per-session request state moves through idle, pending, and running states so invoice and
    narrative controls remain disabled while a request is in flight.
11. Curated local PNG assets provide the page icon and responsive header lockup without a network
    dependency; the Project view owns product story, workflow, trust boundaries, and public links.

Historical intelligence uses timestamped fixture prices and confirmed purchases to construct
comparable snapshots. Market movement excludes the cash effect of purchases made inside the
comparison period; those purchases are reported separately. Daily and weekly narratives consume
serialized KPI contexts and pass through word-count and financial-language guardrails.

SQLite is used locally for traceability and transactional writes. Runtime databases are ignored
by Git. Confirmed invoice purchases retain the source, confirmation timestamp, document reference,
SHA-256, active/voided status, correction timestamp, and correction reason; uploaded bytes are not
persisted. Active records feed portfolio calculations, while voided records remain queryable in the
audit history and can be restored. Batch voiding uses one SQLite update, and synthetic seed
synchronization deliberately preserves correction state. Existing databases receive the new audit
columns through an additive migration. In Docker, `/app/runtime` can be mounted to the named
`ledgerlens-data` volume so confirmed purchases survive container replacement. Credentials,
uploaded PDFs, unconfirmed drafts, UI filters, and session-cached narratives remain outside that
volume. The repository contains synthetic fixtures only.

OpenAI actions are explicit UI operations. Invoice extraction has one in-flight operation per
browser session. Daily and Weekly narratives are generated only after the user selects the live
mode and presses the generation button; the paired result is cached in session state against a
fingerprint of the deterministic contexts and configured model. A changed context invalidates the
cache and returns the UI to the deterministic narrative until the user explicitly generates again.
