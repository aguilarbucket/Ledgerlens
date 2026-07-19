# Demo script

Target duration: under three minutes.

1. State the problem: manual brokerage invoices do not create a trustworthy, explainable ledger.
2. Download the bundled synthetic invoice from Import purchase and upload it back to LedgerLens.
3. For the recorded video, select OpenAI Responses API and run one controlled GPT-5.6 extraction
   using the bundled synthetic PDF. Show the progress state and explain that controls remain locked
   while the request is in flight. For judge self-testing without credentials, use Offline fixture.
4. Follow the Upload, Extract, Review, and Confirm indicator; show confidence, source, warnings,
   privacy policy, and editable fields. Keep `.env`, terminals, and API dashboards out of frame.
5. Demonstrate that clicking save without the confirmation checkbox is rejected.
6. Confirm the purchase and show the dashboard update, filtered read-only history, and document-hash
   traceability.
7. Show allocation, observable value, position cards, unrealized P/L, and price coverage,
   emphasizing that Python performs every calculation.
8. Open Daily Lens and show semantic KPIs, contribution bars, context quality, and the deterministic
   narrative source.
9. Open Weekly Lens and show current/prior/baseline comparison, contribution bars, distribution
   shift, added positions, and best/worst observable day.
10. Explain that GPT-5.6 extracts typed fields and writes guarded narratives, while Python owns all
    financial calculations. Judges do not need a credential and the app never switches models or
    creates a new narrative request on an ordinary UI rerun.

Use only the bundled synthetic PDF and portfolio in the recording. Do not expose `.env`, terminal
history, local paths, account details, or API dashboards.
