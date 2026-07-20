# LedgerLens

LedgerLens is an AI-assisted personal portfolio ledger for converting synthetic brokerage PDFs into
human-verified records and deterministic financial insights. The demo includes five invoices from
distinct fictional brokers. The reproducible judge path runs entirely offline and does not require
an API key.

## Cross-platform quickstart

Run each command as one complete line. These commands work unchanged in Windows PowerShell,
Command Prompt, Bash, and zsh. Host port 8502 avoids the common local Streamlit port 8501:

```console
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run -d --rm --name ledgerlens -p 127.0.0.1:8502:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 alejandroromeroa/ledgerlens:buildweek-2026
```

Open [http://localhost:8502](http://localhost:8502) and stop the application with
`docker stop ledgerlens`.

If Docker reports `port is already allocated`, inspect it with `docker ps --filter publish=8502`.
Stop it only if it is your stale container, or use `-p 127.0.0.1:8503:8501` and open port 8503.

The named volume preserves confirmed SQLite purchases and auditable correction state across
container replacement. Erroneous or duplicate records can be voided and restored without erasing
history; corrections are not represented as sales. Uploaded PDF bytes, unconfirmed drafts, API
credentials, and session-cached narratives are not stored in that volume.

## Project links

- [Public source and complete README](https://github.com/aguilarbucket/Ledgerlens)
- [Judge instructions](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/JUDGE_INSTRUCTIONS.md)
- [Architecture and trust boundaries](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/ARCHITECTURE.md)
- [CVE risk acknowledgement](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/SECURITY_CVE_ACKNOWLEDGEMENT.md)

LedgerLens is released under the MIT License. All bundled portfolio records, companies, prices, and
PDF documents are fictional.
