from types import SimpleNamespace

import pytest

import ledgerlens.ai.openai_client as openai_client_module
from ledgerlens.ai.invoice_extractor import FixtureInvoiceExtractor
from ledgerlens.ai.openai_client import OpenAIResponseError, OpenAIResponsesClient
from ledgerlens.invoices.confirmation import ConfirmationRequiredError, confirm_extraction
from ledgerlens.invoices.models import InvoiceExtraction
from ledgerlens.invoices.pdf_validation import validate_pdf

VALID_PDF = b"%PDF-1.4\nsynthetic content\n%%EOF\n"


def validated_pdf():
    return validate_pdf(filename="synthetic.pdf", mime_type="application/pdf", content=VALID_PDF)


def test_fixture_extraction_requires_human_confirmation() -> None:
    extraction = FixtureInvoiceExtractor().extract(validated_pdf())

    with pytest.raises(ConfirmationRequiredError, match="Human review"):
        confirm_extraction(
            extraction,
            reviewed_and_confirmed=False,
            document_sha256=validated_pdf().sha256,
            source="synthetic_fixture",
        )

    purchase = confirm_extraction(
        extraction,
        reviewed_and_confirmed=True,
        document_sha256=validated_pdf().sha256,
        source="synthetic_fixture",
    )
    assert purchase.document_reference == "SYNTH-BW-2026-005"
    assert purchase.document_sha256 == validated_pdf().sha256
    assert purchase.confirmed_at is not None


class FakeResponses:
    def __init__(self, parsed):
        self.parsed = parsed
        self.kwargs = None

    def parse(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(output_parsed=self.parsed)

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(output_text=self.parsed)


def test_openai_client_can_disable_sdk_retries(monkeypatch) -> None:
    captured = {}

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(responses=FakeResponses(None))

    monkeypatch.setattr(openai_client_module, "OpenAI", fake_openai)
    OpenAIResponsesClient(api_key="synthetic-test-key", max_retries=0)

    assert captured["max_retries"] == 0


def test_openai_client_requires_api_key(monkeypatch) -> None:
    monkeypatch.setattr(openai_client_module, "load_project_environment", lambda: False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(openai_client_module.OpenAIConfigurationError, match="not configured"):
        OpenAIResponsesClient()


def test_openai_client_uses_structured_pdf_request_without_network() -> None:
    extraction = FixtureInvoiceExtractor().extract(validated_pdf())
    responses = FakeResponses(extraction)
    sdk_client = SimpleNamespace(responses=responses)
    client = OpenAIResponsesClient(model="gpt-5.6", sdk_client=sdk_client)

    parsed = client.parse_pdf(
        pdf=validated_pdf(), instructions="Extract fields.", response_model=InvoiceExtraction
    )

    assert parsed == extraction
    assert responses.kwargs["store"] is False
    assert responses.kwargs["model"] == "gpt-5.6"
    content = responses.kwargs["input"][0]["content"]
    assert content[0]["type"] == "input_file"
    assert content[0]["file_data"].startswith("data:application/pdf;base64,")
    assert responses.kwargs["text_format"] is InvoiceExtraction


def test_openai_client_rejects_empty_parsed_response() -> None:
    client = OpenAIResponsesClient(
        model="gpt-5.6", sdk_client=SimpleNamespace(responses=FakeResponses(None))
    )

    with pytest.raises(OpenAIResponseError, match="no parsed"):
        client.parse_pdf(
            pdf=validated_pdf(), instructions="Extract fields.", response_model=InvoiceExtraction
        )


def test_openai_client_generates_text_without_exposing_context_in_logs() -> None:
    responses = FakeResponses("Factual narrative.")
    client = OpenAIResponsesClient(model="gpt-5.6", sdk_client=SimpleNamespace(responses=responses))

    result = client.generate_text(
        instructions="Use facts only.", input_text='{"metric":"value"}', max_output_tokens=100
    )

    assert result == "Factual narrative."
    assert responses.kwargs["store"] is False
    assert responses.kwargs["model"] == "gpt-5.6"
    assert responses.kwargs["input"] == '{"metric":"value"}'
