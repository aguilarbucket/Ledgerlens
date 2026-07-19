from __future__ import annotations

import hashlib
from collections.abc import MutableMapping
from typing import Any

IDLE = "idle"
PENDING = "pending"
RUNNING = "running"
BUSY_STATES = frozenset({PENDING, RUNNING})


def is_request_busy(state: MutableMapping[str, Any], *, state_key: str) -> bool:
    return state.get(state_key, IDLE) in BUSY_STATES


def queue_request(state: MutableMapping[str, Any], *, state_key: str) -> bool:
    """Queue one request unless the current session already has one in flight."""
    if is_request_busy(state, state_key=state_key):
        return False
    state[state_key] = PENDING
    return True


def claim_request(state: MutableMapping[str, Any], *, state_key: str) -> bool:
    """Atomically move a queued request to running for the current session."""
    if state.get(state_key) != PENDING:
        return False
    state[state_key] = RUNNING
    return True


def finish_request(state: MutableMapping[str, Any], *, state_key: str) -> None:
    state[state_key] = IDLE


def request_fingerprint(*parts: str | bytes) -> str:
    """Build a stable, non-secret identifier for request inputs."""
    digest = hashlib.sha256()
    for part in parts:
        encoded = part.encode("utf-8") if isinstance(part, str) else part
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
