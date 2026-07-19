# OpenAI integration

LedgerLens uses one centralized OpenAI Python SDK client and the Responses API. The invoice path
sends the validated PDF as an in-memory Base64 `input_file` plus minimal extraction instructions.
It sets `store=False` and parses directly into a strict Pydantic response model.

Official references checked on July 18, 2026:

- https://developers.openai.com/api/docs/guides/file-inputs
- https://developers.openai.com/api/docs/guides/structured-outputs

The model is configurable through `OPENAI_MODEL` and currently defaults to `gpt-5.6`, matching the
Build Week requirement and current guide examples. The exact model ID was validated successfully
with the project API account on July 18, 2026. LedgerLens never silently switches to an older
model.

Daily Lens and Weekly Lens send only serialized deterministic KPI contexts. Generated text must
pass maximum-word and financial-language guardrails. Empty, excessive, advisory, predictive, or
causal text is rejected and replaced by a clearly labeled deterministic fallback.

## UI request lifecycle

Live operations are initiated only by explicit buttons. While an invoice or paired Daily/Weekly
request is running, its mode selector and action controls are disabled and a multi-step status is
shown. Per-session idle, pending, and running states reject re-entry while the first operation is
in flight. AI Insight results are cached only in Streamlit session state and keyed by a fingerprint
of the deterministic contexts and configured model, preventing ordinary UI reruns from creating
new billable calls. No response cache or unconfirmed draft is written to SQLite.

## Credential boundary

`OPENAI_API_KEY` is read only from the process environment or the ignored project-local `.env`.
Local values never replace explicitly supplied process variables. The key is never accepted
through the UI, logged, stored in SQLite, or committed. Live mode fails explicitly when the key is
absent. Automated tests inject a fake SDK client and make no network calls.

## Controlled live validation

On July 18, 2026, the opt-in validator made exactly three successful Responses API requests with
`gpt-5.6` and bundled synthetic data. Structured PDF extraction passed in 5.835 seconds; Daily Lens
guardrails passed in 4.087 seconds; Weekly Lens guardrails passed in 4.888 seconds. The validator
reported metadata and pass/fail status only. It did not print the key, prompts, PDF body, or model
narratives. Automatic SDK retries are disabled by this validator to preserve its three-attempt
ceiling.
