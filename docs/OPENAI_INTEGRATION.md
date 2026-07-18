# OpenAI integration

LedgerLens uses one centralized OpenAI Python SDK client and the Responses API. The invoice path
sends the validated PDF as an in-memory Base64 `input_file` plus minimal extraction instructions.
It sets `store=False` and parses directly into a strict Pydantic response model.

Official references checked on July 18, 2026:

- https://developers.openai.com/api/docs/guides/file-inputs
- https://developers.openai.com/api/docs/guides/structured-outputs

The model is configurable through `OPENAI_MODEL` and currently defaults to `gpt-5.6`, matching the
Build Week requirement and current guide examples. Availability and the exact accessible model ID
must be validated with the project API account before the first paid request. LedgerLens never
silently switches to an older model.

## Credential boundary

`OPENAI_API_KEY` is read only from the environment. It is never accepted through the UI, logged,
stored in SQLite, or committed. Live mode fails explicitly when the key is absent. Automated tests
inject a fake SDK client and make no network calls.

