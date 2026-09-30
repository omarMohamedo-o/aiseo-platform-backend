"""Integration tests for AI Intelligence & Question Generation API."""
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_generate_questions_success() -> None:
    with _client() as client:
        response = client.post(
            "/api/v1/intelligence/questions/generate",
            json={
                "topic": "Generative Engine Optimization",
                "keywords": ["GEO", "AI Search", "AEO"],
                "lens": "geo",
                "count": 3,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Generative Engine Optimization"
        assert len(data["questions"]) <= 3
        assert len(data["questions"]) > 0

        # Verify question schema
        for q in data["questions"]:
            assert "question" in q
            assert "intent" in q
            assert "funnel_stage" in q
            assert isinstance(q["intent"], str) and q["intent"]
            assert isinstance(q["funnel_stage"], str) and q["funnel_stage"]


def test_generate_questions_validates_topic_length() -> None:
    with _client() as client:
        # Too short topic (<2 chars)
        response = client.post(
            "/api/v1/intelligence/questions/generate",
            json={"topic": "a", "count": 2},
        )
        assert response.status_code == 422


def test_generate_questions_validates_count_range() -> None:
    with _client() as client:
        # Invalid count (>20)
        response = client.post(
            "/api/v1/intelligence/questions/generate",
            json={"topic": "Valid Topic", "count": 50},
        )
        assert response.status_code == 422
