"""Integration tests for AI Visibility & Answer Analysis API."""
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_analyze_answers_endpoint_calculates_visibility_and_citations() -> None:
    with _client() as client:
        payload = {
            "brand": "Anthropic",
            "items": [
                {
                    "prompt_run_id": "test-run-1",
                    "provider": "chatgpt",
                    "question": "What is Claude and who created it?",
                    "answer": "Claude is an advanced AI assistant created by Anthropic. See https://anthropic.com for details.",
                    "citations": ["https://anthropic.com"],
                },
                {
                    "prompt_run_id": "test-run-2",
                    "provider": "perplexity",
                    "question": "Best coding LLMs",
                    "answer": "Leading models include Claude 3.5 Sonnet by Anthropic and GPT-4o. Details: https://anthropic.com/claude",
                    "citations": [],
                },
            ],
        }

        response = client.post("/api/v1/visibility/answers/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        first = data[0]
        assert first["brand"] == "Anthropic"
        assert first["brand_mentioned"] is True
        assert first["visibility_score"] > 50
        assert "https://anthropic.com" in first["extracted_citations"]
        assert first["sentiment"] in ("positive", "neutral", "mixed")


def test_analyze_answers_detects_unmentioned_brand() -> None:
    with _client() as client:
        payload = {
            "brand": "UnicornCorp",
            "items": [
                {
                    "prompt_run_id": "test-run-3",
                    "provider": "gemini",
                    "question": "What is Python?",
                    "answer": "Python is a high-level programming language created by Guido van Rossum.",
                    "citations": ["https://python.org"],
                }
            ],
        }

        response = client.post("/api/v1/visibility/answers/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["brand_mentioned"] is False
        assert data[0]["visibility_score"] <= 25


def test_execute_prompts_matrix() -> None:
    with _client() as client:
        payload = {
            "providers": ["openai"],
            "questions": ["What is Generative Engine Optimization?"],
            "system_prompt": "You are a search expert.",
        }

        response = client.post("/api/v1/visibility/prompts/execute", json=payload)
        assert response.status_code == 200
        results = response.json()
        assert len(results) >= 1
        assert "provider" in results[0]
        assert "status" in results[0]
