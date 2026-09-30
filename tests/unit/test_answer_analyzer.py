"""Unit tests for AnswerAnalyzerService."""
from __future__ import annotations

import pytest

from aiseo.application.analysis.answer_analyzer import (
    AnswerAnalyzerService,
    analyze_deterministic,
    extract_urls_from_text,
)


def test_extract_urls_from_text() -> None:
    text = (
        "Check out https://acme.com/features and also https://docs.acme.com/api. "
        "More info at https://partner.org/blog, and punctuation test https://test.com/link."
    )
    urls = extract_urls_from_text(text)
    assert "https://acme.com/features" in urls
    assert "https://docs.acme.com/api" in urls
    assert "https://partner.org/blog" in urls
    assert "https://test.com/link" in urls


def test_analyze_deterministic_brand_mentioned() -> None:
    answer = (
        "When evaluating the top platforms, Acme Corp is widely considered the best choice. "
        "You can read more at https://acme.com/guide."
    )
    res = analyze_deterministic(
        prompt_run_id="run-1",
        provider="perplexity",
        question="What is the best SEO tool?",
        answer=answer,
        brand="Acme Corp",
    )

    assert res.brand_mentioned is True
    assert res.sentiment == "positive"
    assert res.visibility_score > 55
    assert "https://acme.com/guide" in res.extracted_citations
    assert res.mention_position is not None


def test_analyze_deterministic_brand_not_mentioned() -> None:
    answer = "The top tools on the market are Competitor A and Competitor B."
    res = analyze_deterministic(
        prompt_run_id="run-2",
        provider="chatgpt",
        question="What is the best SEO tool?",
        answer=answer,
        brand="Acme Corp",
    )

    assert res.brand_mentioned is False
    assert res.visibility_score == 0
    assert res.mention_position is None


@pytest.mark.asyncio
async def test_answer_analyzer_service_batch() -> None:
    service = AnswerAnalyzerService(llm_provider=None)
    items = [
        {
            "prompt_run_id": "p1",
            "provider": "openai",
            "question": "Best CRM?",
            "answer": "Acme CRM is an industry leading recommendation.",
            "citations": ["https://acme.com"],
        },
        {
            "prompt_run_id": "p2",
            "provider": "gemini",
            "question": "Best CRM?",
            "answer": "Salesforce and HubSpot dominate the market.",
            "citations": [],
        },
    ]

    results = await service.analyze_answers(brand="Acme", items=items)
    assert len(results) == 2
    assert results[0].brand_mentioned is True
    assert results[0].sentiment == "positive"
    assert results[1].brand_mentioned is False
