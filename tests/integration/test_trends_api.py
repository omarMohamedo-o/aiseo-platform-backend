"""Integration tests for Google Trends & Time Series API."""
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_fetch_trends_series_returns_normalized_points() -> None:
    with _client() as client:
        payload = {
            "terms": ["generative engine optimization", "answer engine optimization", "seo"],
            "geo": "WORLDWIDE",
            "start_date": "12 months ago",
            "category": "all",
        }

        response = client.post("/api/v1/trends/series", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert "points" in data
        assert "configured" in data
        assert "provider" in data
        assert data["terms"] == ["generative engine optimization", "answer engine optimization", "seo"]


def test_fetch_trends_series_rejects_empty_terms() -> None:
    with _client() as client:
        response = client.post("/api/v1/trends/series", json={"terms": []})
        assert response.status_code == 422
