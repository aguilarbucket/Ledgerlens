from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FieldConfidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: float = Field(ge=0, le=1)
    ticker: float = Field(ge=0, le=1)
    quantity: float = Field(ge=0, le=1)
    unit_price: float = Field(ge=0, le=1)
    purchase_date: float = Field(ge=0, le=1)
    platform: float = Field(ge=0, le=1)
    currency: float = Field(ge=0, le=1)
    document_reference: float = Field(ge=0, le=1)


class InvoiceExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str = Field(min_length=1, max_length=120)
    ticker: str = Field(min_length=1, max_length=30)
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)
    purchase_date: date
    platform: str = Field(min_length=1, max_length=120)
    currency: Literal["CLP"]
    document_reference: str | None = Field(default=None, max_length=120)
    confidence: FieldConfidence
    warnings: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("company", "ticker", "platform")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value cannot be blank.")
        return cleaned

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.upper()

    @field_validator("document_reference")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None
