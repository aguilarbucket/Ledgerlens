from __future__ import annotations

import base64
import logging
import os
import time
from typing import Any

from openai import OpenAI
from pydantic import BaseModel

from ledgerlens.invoices.pdf_validation import ValidatedPDF

logger = logging.getLogger(__name__)


class OpenAIConfigurationError(RuntimeError):
    """Raised when the live OpenAI integration is not configured."""


class OpenAIResponseError(RuntimeError):
    """Raised when OpenAI does not return a parsed structured response."""


class OpenAIResponsesClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 60,
        sdk_client: Any | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_key and sdk_client is None:
            raise OpenAIConfigurationError("OPENAI_API_KEY is not configured.")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.6")
        self.timeout_seconds = timeout_seconds
        self._client = sdk_client or OpenAI(api_key=resolved_key, timeout=timeout_seconds)

    def parse_pdf(
        self,
        *,
        pdf: ValidatedPDF,
        instructions: str,
        response_model: type[BaseModel],
    ) -> BaseModel:
        encoded = base64.b64encode(pdf.content).decode("ascii")
        started = time.perf_counter()
        status = "error"
        try:
            response = self._client.responses.parse(
                model=self.model,
                store=False,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_file",
                                "filename": pdf.filename,
                                "file_data": f"data:application/pdf;base64,{encoded}",
                            },
                            {"type": "input_text", "text": instructions},
                        ],
                    }
                ],
                text_format=response_model,
                timeout=self.timeout_seconds,
            )
            parsed = response.output_parsed
            if parsed is None:
                raise OpenAIResponseError("OpenAI returned no parsed invoice extraction.")
            status = "ok"
            return parsed
        finally:
            logger.info(
                "OpenAI response model=%s latency_seconds=%.3f status=%s",
                self.model,
                time.perf_counter() - started,
                status,
            )

    def generate_text(
        self,
        *,
        instructions: str,
        input_text: str,
        max_output_tokens: int,
    ) -> str:
        started = time.perf_counter()
        status = "error"
        try:
            response = self._client.responses.create(
                model=self.model,
                store=False,
                instructions=instructions,
                input=input_text,
                max_output_tokens=max_output_tokens,
                timeout=self.timeout_seconds,
            )
            text = response.output_text.strip() if response.output_text else ""
            if not text:
                raise OpenAIResponseError("OpenAI returned no analyst narrative.")
            status = "ok"
            return text
        finally:
            logger.info(
                "OpenAI response model=%s latency_seconds=%.3f status=%s",
                self.model,
                time.perf_counter() - started,
                status,
            )

