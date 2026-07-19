# Judge instructions

LedgerLens runs as a fully synthetic offline demonstration. No API key, private account, broker
connection, or external market service is required for the reproducible judge path.

## Option A — Public container image

Requirements: Docker Desktop or Docker Engine with the Docker CLI.

```bash
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run --rm --name ledgerlens -p 8501:8501 \
  --mount type=volume,source=ledgerlens-data,target=/app/runtime \
  alejandroromeroa/ledgerlens:buildweek-2026
```

Open `http://localhost:8501`. Stop the application with `Ctrl+C`. The named volume preserves only
confirmed SQLite purchases across container replacement. Uploaded PDF bytes, unconfirmed drafts,
API credentials, and session-cached narratives are not written to the volume.

If port 8501 is already in use, replace `-p 8501:8501` with `-p 8502:8501` and open
`http://localhost:8502`.

## Option B — Build from the public source repository

Requirements: Git and Docker.

```bash
git clone https://github.com/aguilarbucket/Ledgerlens.git
cd Ledgerlens
docker compose up --build
```

Open `http://localhost:8501`. Stop with `Ctrl+C`, then run `docker compose down`. Do not add an
`.env` file for the offline judge path.

## Five-minute verification path

1. Confirm the **Synthetic demo** banner on Portfolio.
2. Open **Import purchase** and download the bundled synthetic invoice.
3. Upload the same PDF, keep **Offline fixture**, and select **Validate and extract**.
4. Confirm that the source, field confidence, warning, document hash, and editable review appear.
5. Attempt to save without the confirmation checkbox and observe the rejection.
6. Select the confirmation checkbox, save, and verify the updated Portfolio and Purchase history.
7. Open **AI Insights** and inspect Daily Lens and Weekly Lens deterministic KPIs, quality status,
   contribution charts, and narrative source labels.
8. Select **OpenAI Responses API** only to confirm that generation is an explicit action. No live
   request is required and no fallback model is selected silently.

## Expected boundaries

- Every displayed company, price, purchase, platform, and PDF is fictional.
- Python calculates all portfolio metrics; GPT-5.6 is limited to typed extraction and guarded text.
- Saving an extracted record requires explicit human confirmation.
- The uploaded PDF is processed in memory and is never persisted.
- The demo does not trade, recommend, predict prices, or claim realized gains.

## Public artifacts

- Source: https://github.com/aguilarbucket/Ledgerlens
- Container: https://hub.docker.com/r/alejandroromeroa/ledgerlens
- License: MIT
