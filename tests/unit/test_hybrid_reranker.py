"""Unit tests for Hybrid Search (BM25 + Dense) and Cross-Encoder Reranking (Stage 12 / Stage B)."""
import pytest
from fastapi.testclient import TestClient

from aiseo.adapters.retrieval.hybrid_reranker_adapter import HybridRerankerAdapter
from aiseo.api.app import create_app
from aiseo.domain.evaluation.rerank import RerankCandidate
from aiseo.infrastructure.configuration.settings import Settings


@pytest.mark.asyncio
async def test_bm25_lexical_scoring() -> None:
    adapter = HybridRerankerAdapter()
    query = "enterprise analytics pricing"
    corpus = [
        "The weather is very sunny today in San Francisco.",
        "Enterprise analytics pricing starts at $99 per user per month with unlimited dashboards.",
        "We offer standard cloud hosting and database administration.",
    ]
    scores = adapter._score_bm25(query, corpus)
    assert len(scores) == 3
    # Passage 2 has the highest match
    assert scores[1] > scores[0]
    assert scores[1] > scores[2]


@pytest.mark.asyncio
async def test_hybrid_reranking_rrf() -> None:
    adapter = HybridRerankerAdapter()
    query = "SOC2 compliance security"
    candidates = [
        RerankCandidate(
            text="General marketing strategies for startups.",
            dense_vector_score=0.2,
        ),
        RerankCandidate(
            text="Our platform enforces SOC2 compliance and zero-trust security architecture.",
            dense_vector_score=0.92,
        ),
        RerankCandidate(
            text="Employee benefits and open positions at our company.",
            dense_vector_score=0.1,
        ),
    ]

    ranked = await adapter.rerank(query, candidates, top_k=2)
    assert len(ranked) == 2
    assert "SOC2" in ranked[0].text
    assert ranked[0].final_score > ranked[1].final_score


@pytest.mark.asyncio
async def test_predict_aeo_snippet() -> None:
    adapter = HybridRerankerAdapter()
    question = "What is ExampleCorp?"
    passages = [
        "ExampleCorp is an enterprise AI search visibility platform. "
        "It provides real-time brand mention tracking, citation link verification, "
        "and automated hallucination defense for modern marketing teams. "
        "The software integrates with ChatGPT, Google Gemini, and Perplexity.",
    ]

    pred = await adapter.predict_aeo_snippet(
        question=question,
        passages=passages,
        brand="ExampleCorp",
    )

    assert pred.question == question
    assert "ExampleCorp is an enterprise AI search visibility platform" in pred.predicted_snippet
    assert pred.word_count > 15
    assert pred.confidence >= 0.70
    assert pred.recommended_heading is not None


def test_predict_snippet_api_endpoint() -> None:
    app = create_app(settings=Settings())
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/intelligence/snippets/predict",
            json={
                "question": "What is ExampleCorp?",
                "brand": "ExampleCorp",
                "passages": [
                    "ExampleCorp is a modern generative engine optimization platform. "
                    "It monitors brand citations and optimizes search visibility across AI engines."
                ],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == "What is ExampleCorp?"
        assert "ExampleCorp is a modern" in data["predicted_snippet"]
        assert data["confidence"] > 0.5

