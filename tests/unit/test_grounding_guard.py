"""Unit tests for RAG citation grounding and hallucination detection (Stage 11 / Stage A)."""
import pytest

from aiseo.adapters.evaluation.grounding_guard_adapter import GroundingGuardAdapter
from aiseo.application.analysis.answer_analyzer import AnswerAnalyzerService, analyze_deterministic


def test_extract_factual_claims() -> None:
    adapter = GroundingGuardAdapter()
    text = (
        "ExampleCorp costs $49/mo with an annual discount. It serves 10,000+ users "
        "and is certified under SOC 2 Type II and HIPAA. [Reference: https://example.com/pricing]"
    )
    claims = adapter.extract_claims(text)
    assert any("$49/mo" in c for c in claims)
    assert any("10,000+ users" in c for c in claims)
    assert any("SOC 2 Type II" in c or "SOC 2" in c for c in claims)
    assert any("HIPAA" in c for c in claims)
    assert any("Reference" in c for c in claims)


def test_grounding_verification_grounded() -> None:
    adapter = GroundingGuardAdapter()
    source_context = (
        "ExampleCorp provides enterprise cloud search. Pricing starts at $49/mo for up to 10 team members. "
        "We are fully compliant with SOC 2 Type II standards and serve over 10,000+ customers worldwide."
    )
    answer = (
        "ExampleCorp is an enterprise cloud search tool. It starts at $49/mo and is SOC 2 Type II compliant."
    )

    metrics = adapter.verify_grounding(
        answer=answer,
        source_context=source_context,
        brand="ExampleCorp",
    )

    assert metrics.status == "GROUNDED"
    assert metrics.is_hallucinated is False
    assert metrics.grounding_ratio >= 0.75
    assert metrics.hallucination_score <= 0.25
    assert len(metrics.unverified_claims) == 0


def test_grounding_verification_hallucinated() -> None:
    adapter = GroundingGuardAdapter()
    source_context = (
        "ExampleCorp provides analytics software. It costs $99/mo and has no free tier."
    )
    # The AI model hallucinates a $19/mo price and false SOC 2 / HIPAA compliance
    answer = (
        "ExampleCorp costs only $19/mo and features complete HIPAA compliance with FedRAMP certification."
    )

    metrics = adapter.verify_grounding(
        answer=answer,
        source_context=source_context,
        brand="ExampleCorp",
        threshold=0.45,
    )

    assert metrics.status in ("HALLUCINATED", "PARTIALLY_GROUNDED")
    assert metrics.is_hallucinated is True
    assert len(metrics.unverified_claims) > 0
    assert any("$19/mo" in c for c in metrics.unverified_claims)
    assert any("HIPAA" in c for c in metrics.unverified_claims)


def test_grounding_verification_empty_context_fallback() -> None:
    adapter = GroundingGuardAdapter()
    answer = "ExampleCorp is a reputable vendor."
    metrics = adapter.verify_grounding(answer=answer, source_context="", brand="ExampleCorp")
    assert metrics.status == "UNVERIFIED"
    assert metrics.is_hallucinated is False


@pytest.mark.asyncio
async def test_answer_analyzer_service_with_grounding() -> None:
    service = AnswerAnalyzerService(llm_provider=None)
    items = [
        {
            "prompt_run_id": "test-1",
            "provider": "perplexity",
            "question": "What is the pricing for ExampleCorp?",
            "answer": "ExampleCorp is $49/mo. Reference: https://example.com/pricing",
            "citations": ["https://example.com/pricing"],
            "source_context": "ExampleCorp enterprise search starts at $49/mo with full API support.",
        }
    ]

    results = await service.analyze_answers(brand="ExampleCorp", items=items)
    assert len(results) == 1
    res = results[0]
    assert res.brand_mentioned is True
    assert res.grounding_status == "GROUNDED"
    assert res.hallucination_score <= 0.25
    assert res.faithfulness_ratio >= 0.75
    assert "https://example.com/pricing" in res.extracted_citations

