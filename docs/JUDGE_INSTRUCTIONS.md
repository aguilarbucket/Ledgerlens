# Judge instructions

LedgerLens runs as a fully synthetic offline demonstration. No API key, private account, broker
connection, or external market service is required for the reproducible judge path.

## Option A — Public container image

Requirements: Docker Desktop or Docker Engine with the Docker CLI.

These commands work unchanged in Windows PowerShell, Command Prompt, Bash, and zsh. Run each command
as one complete line; PowerShell does not use the Bash `\` line-continuation character. This path
uses host port 8502 to avoid collisions with local Streamlit or Docker Compose processes on 8501.

```console
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run -d --rm --name ledgerlens -p 127.0.0.1:8502:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 alejandroromeroa/ledgerlens:buildweek-2026
```

Open `http://localhost:8502`. Confirm the container with `docker ps --filter name=ledgerlens` and
stop it with `docker stop ledgerlens`. The named volume preserves only confirmed SQLite purchases
across container replacement. Uploaded PDF bytes, unconfirmed drafts, API credentials, and
session-cached narratives are not written to the volume.

If Docker reports `port is already allocated`, run `docker ps --filter publish=8502` to identify
the process using the documented host port. Stop it only if it is your stale container, or rerun
with `-p 127.0.0.1:8503:8501` and open `http://localhost:8503`. For a container-name conflict,
inspect `docker ps -a --filter name=ledgerlens` before stopping or removing anything.

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
2. Open **Import purchase**, choose one of five fictional broker invoices, and download it.
3. Upload the same PDF, keep **Offline fixture**, and select **Validate and extract**.
4. Confirm that the source, field confidence, warning, document hash, and editable review appear.
5. Attempt to save without the confirmation checkbox and observe the rejection.
6. Select the confirmation checkbox, save, and verify the updated Portfolio and Purchase history.
7. Open **AI Insights** and inspect Daily Lens and Weekly Lens deterministic KPIs, quality status,
   contribution charts, and narrative source labels.
8. Select **OpenAI Responses API** only to confirm that generation is an explicit action. No live
   request is required and no fallback model is selected silently.
9. Open **Project** to review the multi-broker origin story, four-step workflow, trust controls,
   Python/OpenAI responsibility boundary, current limitations, and public project links.

Optional correction check: open **Purchase history** and expand **Manage ledger records**. Select
one active record or all active lots for its ticker, choose an error/duplicate reason, acknowledge
that this is not a sale, and void it. The Portfolio excludes the correction while Purchase history
retains it under the **Voided** status. The same panel can restore the record.

## Expected boundaries

- Every displayed company, price, purchase, platform, and PDF is fictional.
- Python calculates all portfolio metrics; GPT-5.6 is limited to typed extraction and guarded text.
- Saving an extracted record requires explicit human confirmation.
- Corrections preserve an audit record; they do not model a sale or realized P/L.
- The uploaded PDF is processed in memory and is never persisted.
- The demo does not trade, recommend, predict prices, or claim realized gains.

## Public artifacts

- Source: https://github.com/aguilarbucket/Ledgerlens
- Container: https://hub.docker.com/r/alejandroromeroa/ledgerlens
- License: MIT
