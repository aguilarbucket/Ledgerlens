# LedgerLens

LedgerLens is an AI-assisted personal portfolio ledger for converting synthetic brokerage PDFs into
human-verified records and deterministic financial insights. The reproducible judge path runs
entirely offline and does not require an API key.

## Cross-platform quickstart

Run each command as one complete line. These commands work unchanged in Windows PowerShell,
Command Prompt, Bash, and zsh:

```console
docker pull alejandroromeroa/ledgerlens:buildweek-2026
docker volume create ledgerlens-data
docker run --rm --name ledgerlens -p 127.0.0.1:8501:8501 --mount "type=volume,source=ledgerlens-data,target=/app/runtime" --read-only --tmpfs "/tmp:rw,noexec,nosuid,size=64m" --cap-drop=ALL --security-opt=no-new-privileges:true --pids-limit=256 --memory=1g --cpus=2 alejandroromeroa/ledgerlens:buildweek-2026
```

Open [http://localhost:8501](http://localhost:8501) and stop the application with `Ctrl+C`.

The named volume preserves confirmed SQLite purchases across container replacement. Uploaded PDF
bytes, unconfirmed drafts, API credentials, and session-cached narratives are not stored in that
volume.

## Project links

- [Public source and complete README](https://github.com/aguilarbucket/Ledgerlens)
- [Judge instructions](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/JUDGE_INSTRUCTIONS.md)
- [Architecture and trust boundaries](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/ARCHITECTURE.md)
- [CVE risk acknowledgement](https://github.com/aguilarbucket/Ledgerlens/blob/main/docs/SECURITY_CVE_ACKNOWLEDGEMENT.md)

LedgerLens is released under the MIT License. All bundled portfolio records, companies, prices, and
PDF documents are fictional.
