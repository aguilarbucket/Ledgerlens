from ledgerlens.ui.request_state import (
    claim_request,
    finish_request,
    is_request_busy,
    queue_request,
    request_fingerprint,
)


def test_request_can_only_be_queued_and_claimed_once_while_busy() -> None:
    state: dict[str, object] = {}

    assert queue_request(state, state_key="invoice") is True
    assert is_request_busy(state, state_key="invoice") is True
    assert queue_request(state, state_key="invoice") is False
    assert claim_request(state, state_key="invoice") is True
    assert claim_request(state, state_key="invoice") is False
    assert queue_request(state, state_key="invoice") is False

    finish_request(state, state_key="invoice")

    assert is_request_busy(state, state_key="invoice") is False
    assert queue_request(state, state_key="invoice") is True


def test_request_fingerprint_is_stable_and_preserves_part_boundaries() -> None:
    assert request_fingerprint("invoice", b"pdf") == request_fingerprint("invoice", b"pdf")
    assert request_fingerprint("ab", "c") != request_fingerprint("a", "bc")
