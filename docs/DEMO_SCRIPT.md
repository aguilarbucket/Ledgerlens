# Build Week demo video script

Target duration: 2 minutes 45 seconds. Hard stop: 2 minutes 50 seconds.

The spoken script is in English so the video satisfies the submission language requirement without
needing a separate translation. Read it naturally rather than rushing to fill every second.

## 0:00-0:18 - Problem and audience

**On screen:** LedgerLens title, then the Portfolio overview with platform distribution visible.

**Narration:**

> As an amateur investor, I use more than one brokerage. Each broker has a different dashboard,
> which makes it difficult to see one clear history of my purchases and portfolio. I built
> LedgerLens to consolidate that workflow without turning a simple tracking task into an
> overwhelming trading terminal.

## 0:18-0:38 - Unified synthetic portfolio

**On screen:** Scroll through KPI cards, position allocation, portfolio value, and the four
fictional platforms in Platform distribution.

**Narration:**

> LedgerLens starts with a unified portfolio ledger. This demo uses only fictional companies,
> prices, transactions, and brokers. Python calculates invested value, current value, allocation,
> price coverage, and unrealized profit or loss. The model never owns those calculations.

## 0:38-0:58 - Select and upload an invoice

**On screen:** Open Import purchase, show the five sample choices, select Corredora Demo, download
the PDF, and upload it back to LedgerLens. Select OpenAI Responses API.

**Narration:**

> Five synthetic brokerage invoices are bundled for reproducible testing. They use different
> brokers, tickers, dates, quantities, and amounts. I will use this sample to demonstrate the live
> GPT-5.6 path. Judges can reproduce the same workflow offline without an API key.

## 0:58-1:23 - GPT-5.6 structured extraction

**On screen:** Select Validate and extract. Keep the progress status and disabled controls visible
until the editable result appears.

**Narration:**

> LedgerLens validates the PDF type, size, signature, and end marker before sending it in memory to
> GPT-5.6 through the OpenAI Responses API. GPT-5.6 returns a strict typed draft with the company,
> ticker, quantity, price, date, broker, currency, reference, confidence, and warnings. The request
> is locked while it runs, so a repeated click cannot create a duplicate billable call.

## 1:23-1:47 - Human confirmation and privacy

**On screen:** Show source metadata, confidence, and editable fields. Briefly trigger the rejection
without checking confirmation, then select the checkbox and save.

**Narration:**

> The extraction is never saved automatically. A person can correct every field, and LedgerLens
> rejects the save until explicit confirmation is checked. The uploaded PDF is not retained. Only
> the confirmed purchase and its SHA-256 fingerprint enter the persistent SQLite ledger.

## 1:47-2:08 - Portfolio and intelligence

**On screen:** Return to Portfolio to show the update, then show Purchase history, Daily Lens, and
Weekly Lens without lingering on every chart.

**Narration:**

> The confirmed record immediately updates the portfolio and remains available after the container
> is replaced. Daily and Weekly Lens explain observable contribution, concentration, data quality,
> and period comparisons. GPT-5.6 may describe those precomputed facts, while guardrails reject
> advice, predictions, invented causes, and realized-gain claims.

## 2:08-2:34 - Codex collaboration and human decisions

**On screen:** Briefly show the Codex task or a clean GitHub view of the changelog and architecture;
do not show local paths, terminals containing secrets, or `.env`.

**Narration:**

> Codex was my primary engineering collaborator. It audited the pre-existing baseline, helped me
> create an independent sanitized repository, designed the modular architecture, implemented and
> tested the invoice and analyst workflows, iterated on the fintech interface, and verified the
> public Docker release. I made the product, privacy, financial-safety, API-budget, design,
> licensing, and publication decisions.

## 2:34-2:48 - Closing

**On screen:** Return to the completed Portfolio overview and LedgerLens title.

**Narration:**

> LedgerLens turns fragmented brokerage evidence into one human-verified portfolio record. It is a
> small tool built for my own tracking problem that can also help other individual investors who
> want a simpler, explainable view across brokers.

## Recording checklist

- Use a fresh synthetic video volume so the save visibly changes the portfolio.
- Confirm `OPENAI_MODEL=gpt-5.6` before recording, but never show `.env`, the API key, usage pages,
  terminal history, local paths, or personal account details.
- Use the default `ledgerlens_synthetic_invoice.pdf` for the controlled live extraction because it
  matches the previously validated reference `SYNTH-BW-2026-005`.
- Record at 1080p with the browser zoom chosen before recording; avoid zoom changes mid-video.
- Keep third-party logos, dashboards, music, and copyrighted material out of frame.
- Use original voice or accurate AI-assisted narration. Add English captions if possible.
- Upload to YouTube as **Public**, not Unlisted or Private.
- Verify final duration is below three minutes and target 2:45-2:50.
- Watch the public YouTube URL in a private browser window before adding it to Devpost.
