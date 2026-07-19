# Fintech UI implementation

## Outcome

LedgerLens now uses a reusable, offline-first fintech interface while preserving the P0 financial,
privacy, and confirmation boundaries. The visual layer never calculates portfolio truth: it
receives typed deterministic results and reshapes them into cards, tables, and chart records.

## Visual system

| Token | Value | Purpose |
| --- | --- | --- |
| Background | `#08111F` | Primary dark canvas |
| Surface | `#111B2E` | Cards and panels |
| Elevated surface | `#16233A` | Emphasized cards |
| Border | `#263653` | Low-contrast structure |
| Primary | `#4F8CFF` | Navigation and primary information |
| Secondary | `#2DD4BF` | Supporting series and verified status |
| Positive | `#22C55E` | Positive financial movement only |
| Negative | `#F87171` | Negative financial movement only |
| Warning | `#F5B942` | Partial context and caution |
| Primary text | `#F8FAFC` | Main content |
| Muted text | `#94A3B8` | Labels and supporting copy |

Green is not the product's primary color; it remains reserved for positive outcomes. Direction is
also written as Positive, Negative, or Neutral so meaning never depends on color alone.

## Implementation boundaries

- `ledgerlens/ui/theme.py` owns tokens, responsive rules, focus treatment, and reduced-motion
  handling.
- `ledgerlens/ui/components.py` owns escaped HTML primitives for headings, KPI and position cards,
  workflow progress, confidence, source metadata, quality, and chart legends.
- `ledgerlens/ui/charts.py` owns Altair specifications and consumes display records only.
- `ledgerlens/ui/view_models.py` converts typed deterministic outputs into chart-shaped records.
- `ledgerlens/ui/portfolio.py`, `insights.py`, and `history.py` compose product views.
- `ledgerlens/analytics/portfolio_dashboard.py` calculates historical values and platform
  allocation so those calculations do not leak into UI code.

The invoice path still requires explicit confirmation. Uploaded PDF bytes are processed in memory
and are not persisted. History is read-only; no edit or delete operation was added.

## Implemented product surfaces

- Portfolio overview with semantic KPIs, current allocation, observable current/invested history,
  position cards, platform distribution, and a detailed table fallback.
- Daily Lens with deterministic contribution bars, narrative source, context quality, contributor
  highlights, concentration, and record counts.
- Weekly Lens with current/prior/baseline comparison, contribution bars, allocation shift,
  best/worst observable days, record integrity, and context quality.
- Invoice import with Upload, Extract, Review, and Confirm progress; explicit offline/OpenAI source;
  editable two-column review; field confidence; and privacy explanation.
- Purchase history with read-only date, ticker, platform, and source filters plus visible-record
  summaries.
- Invoice and AI Insight operations with visible stage progress, disabled in-flight controls,
  explicit completion/error states, and per-session duplicate-request rejection.
- Explicit AI Insight generation with context/model fingerprint caching; ordinary Streamlit
  reruns continue to display deterministic text instead of issuing model requests.

## Executed verification — 2026-07-18

| Check | Result |
| --- | --- |
| `python -m pytest` | 67 tests passed |
| `python -m ruff check .` | Passed |
| Python compilation | Passed |
| Streamlit AppTest | Passed; seven top-level/nested tabs and five charts discovered |
| Responsive browser checks | 390, 768, and 1280 px; document width matched viewport |
| Mandatory confirmation | Unchecked save rejected; checked save passed |
| Portfolio refresh | Invested value changed from 356,000 to 494,000 CLP |
| PDF privacy | Success state confirmed PDF was not persisted; SHA-256 retained |
| Browser console | No error-level messages; transient Vega warnings during tab rerenders only |
| Docker build | `ledgerlens:buildweek-ui` built successfully |
| Container health | HTTP 200 with `ok` |
| Container privilege | UID 999 |
| Container UI | Portfolio and all visual components rendered from the built image |
| Request controls | Synthetic PDF extraction completed with status feedback and editable review |
| Explicit AI mode | Selecting OpenAI mode exposed a Generate button without issuing a request |
| Volume persistence | Four synthetic records written in one container and read in a second |

All executed browser data came from the bundled synthetic portfolio and PDF. No OpenAI request,
yfinance request, Telegram action, deployment, remote push, or publication occurred.
