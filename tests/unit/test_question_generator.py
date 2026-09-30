"""Unit tests for QuestionGeneratorService."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aiseo.application.analysis.question_generator import QuestionGeneratorService
from aiseo.ports.llm.llm_provider import LlmProvider, LlmResponse


class MockLlmProvider(LlmProvider):
    async def generate(self, request):  # type: ignore[no-untyped-def]
        return LlmResponse(text="Mock", model="mock", provider="mock", input_tokens=10, output_tokens=10)

    async def generate_structured(self, request, schema):  # type: ignore[no-untyped-def]
        return schema(
            questions=[
                {
                    "question": "Which enterprise CRM has the highest generative search share?",
                    "intent": "commercial",
                    "funnel_stage": "consideration",
                    "rationale": "High value buyer intent",
                },
                {
                    "question": "How to optimize technical SEO for AI Overviews?",
                    "intent": "implementation",
                    "funnel_stage": "decision",
                    "rationale": "Technical decision maker",
                },
            ]
        )


@pytest.mark.asyncio
async def test_question_generator_success() -> None:
    provider = MockLlmProvider()
    service = QuestionGeneratorService(llm_provider=provider)

    result = await service.generate_questions(
        topic="Enterprise SEO",
        keywords=["ai search", "geo", "aeo"],
        lens="geo",
        count=2,
    )

    assert result.topic == "Enterprise SEO"
    assert len(result.questions) == 2
    assert result.questions[0].intent == "commercial"
    assert result.questions[0].funnel_stage == "consideration"
    assert "CRM" in result.questions[0].question


@pytest.mark.asyncio
async def test_question_generator_fallback_on_llm_failure() -> None:
    mock_failing_llm = AsyncMock(spec=LlmProvider)
    mock_failing_llm.generate_structured.side_effect = RuntimeError("API unavailable")

    service = QuestionGeneratorService(llm_provider=mock_failing_llm)
    result = await service.generate_questions(
        topic="Cloud Storage",
        keywords=["storage"],
        count=3,
    )

    assert result.topic == "Cloud Storage"
    assert len(result.questions) == 3
    assert result.questions[0].intent == "informational"
    assert "Cloud Storage" in result.questions[0].question
