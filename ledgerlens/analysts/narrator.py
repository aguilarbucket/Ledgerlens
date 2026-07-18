from __future__ import annotations

from ledgerlens.ai.openai_client import OpenAIResponsesClient


class OpenAINarrativeProvider:
    def __init__(self, client: OpenAIResponsesClient) -> None:
        self._client = client

    def generate(self, *, instructions: str, context: str, max_output_tokens: int) -> str:
        return self._client.generate_text(
            instructions=instructions,
            input_text=context,
            max_output_tokens=max_output_tokens,
        )
