from __future__ import annotations

from decimal import Decimal


def clp(value: Decimal | None) -> str:
    if value is None:
        return "Not available"
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.0f} CLP".replace(",", ".")


def percent(value: Decimal | None) -> str:
    return "Not available" if value is None else f"{value:.2f}%"


def signed_clp(value: Decimal | None) -> str:
    if value is None:
        return "Not available"
    sign = "+" if value > 0 else ""
    return f"{sign}{clp(value)}"


def signed_percent(value: Decimal | None) -> str:
    if value is None:
        return "Not available"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def semantic_movement(value: Decimal | None) -> str:
    if value is None or value == 0:
        return "Neutral"
    return "Positive" if value > 0 else "Negative"
