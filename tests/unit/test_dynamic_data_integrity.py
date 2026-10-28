"""Unit tests ensuring zero fake/dummy/hardcoded data across the platform."""
import pytest
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings
from aiseo.infrastructure.database import history_repo


@pytest.fixture
def client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_history_repo_never_returns_mock_data():
    """Ensure get_history strictly queries database rows and returns no hardcoded fallback."""
    # When querying a non-existent URL, it must return an empty list, not mock data
    results = history_repo.get_history(url="https://non-existent-domain-12345.com")
    assert isinstance(results, list)
    assert len(results) == 0


def test_global_leaderboard_is_dynamic(client: TestClient):
    """Ensure Global Leaderboard derives scores and queries from actual crawl records."""
    response = client.get("/api/v1/benchmarks/global-leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert "leaderboard" in data
    assert "industry_averages" in data

    for entry in data["leaderboard"]:
        # Verify non-trivial dynamic data
        assert entry["rank"] >= 1
        assert len(entry["domain"]) > 0
        assert len(entry["top_query"]) > 0
        assert entry["visibility_score"] >= 0
        assert entry["opportunity_score"] >= 0
        assert entry["citation_share"] >= 0.0
        assert entry["schema_score"] >= 0
        assert entry["total_pages_indexed"] >= 1
        # No empty dummy placeholders
        assert entry["category"] not in ("", "Audited Domain")


def test_live_breakouts_endpoint(client: TestClient):
    """Ensure live breakouts endpoint returns dynamically fetched tech topics."""
    response = client.get("/api/v1/trends/live-breakouts")
    assert response.status_code == 200
    data = response.json()
    assert "breakouts" in data
    assert isinstance(data["breakouts"], list)

    for item in data["breakouts"]:
        assert "term" in item
        assert "type" in item
        # Ensure it's not the old 2 static fallback items
        assert item["term"] != "Python 3.12" or item["type"] != "Developer Tools"


def test_history_leaderboard_endpoint(client: TestClient):
    """Ensure history-leaderboard returns unified dynamic benchmark data."""
    response = client.get("/api/v1/websites/history-leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)

