# Submission checklist

## Build and privacy

- [x] Independent sanitized repository created.
- [x] Protected baseline documented with maintenance-state hash.
- [x] Synthetic offline portfolio slice runs without credentials.
- [x] Initial tests, lint, compilation, and Streamlit smoke test pass.
- [x] Synthetic invoice PDF is generated and visually verified from fictional data.
- [x] PDF extraction requires editable preview and explicit confirmation.
- [x] Daily Lens and Weekly Lens are visible in Streamlit with deterministic offline reports.
- [x] Controlled GPT-5.6 extraction and Daily/Weekly narrative smoke checks pass on synthetic data.
- [x] Full P0 test matrix passes from a clean environment.
- [x] Final secret, path, data, and dependency review passes; external CVE query timeout is noted.
- [x] Long-running OpenAI controls expose progress and reject duplicate in-flight requests.
- [x] AI Insights require an explicit action and reuse a context-bound session result.
- [x] Confirmed purchases persist across container replacement through a named Docker volume.
- [x] Uploaded PDFs, unconfirmed drafts, and credentials remain outside persistent storage.

## Devpost materials

- [x] MIT license selected and included in the repository.
- [x] Official GitHub and Docker Hub targets are documented with exact judge commands.
- [ ] English project description finalized.
- [ ] Public demo video with audio is under three minutes.
- [x] Repository is public with MIT licensing and accessible to judges.
- [x] README explains Codex, GPT-5.6, and human decisions.
- [ ] Majority-work Codex thread Session ID captured through `/feedback`.
- [ ] Submission instructions and all claims match verified behavior.
