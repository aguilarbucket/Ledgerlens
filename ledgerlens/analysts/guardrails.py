from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol


class NarrativeProvider(Protocol):
    def generate(self, *, instructions: str, context: str, max_output_tokens: int) -> str: ...


@dataclass(frozen=True, slots=True)
class AnalystReport:
    text: str
    source: str
    warning: str | None = None


PROHIBITED_PATTERNS = (
    r"\b(buy|sell|hold)\b",
    r"\b(recommend|recommendation|should)\b",
    r"\b(predict|prediction|forecast|will)\b",
    r"\b(because|caused by|due to)\b",
)


def validate_narrative(text: str, *, max_words: int) -> None:
    if not text.strip():
        raise ValueError("Narrative is empty.")
    if len(text.split()) > max_words:
        raise ValueError(f"Narrative exceeds {max_words} words.")
    for pattern in PROHIBITED_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            raise ValueError("Narrative violates financial language guardrails.")
