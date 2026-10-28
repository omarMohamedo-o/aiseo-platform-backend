"""Unit tests for the Free & Open-Source Ground Truth Verification Engine."""
import pytest
from fastapi.testclient import TestClient

from aiseo.adapters.evaluation.free_ground_truth_adapter import FreeGroundTruthAdapter
from aiseo.api.app import create_app
from aiseo.domain.evaluation.ground_truth import GroundTruthValidationResult
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


@pytest.mark.asyncio
async def test_ground_truth_adapter_live_or_structured():
    adapter = FreeGroundTruthAdapter(timeout=4.0)
    result = await adapter.verify_domain(
        domain="stripe.com",
        brand="Stripe",
        keywords=["payments", "billing"],
    )

    assert isinstance(result, GroundTruthValidationResult)
    assert result.domain == "stripe.com"
    assert result.brand == "Stripe"
    assert result.overall_empirical_confidence >= 0
    assert result.verdict in ("HIGH_CONFIDENCE_GROUND_TRUTH", "MODERATE_CONFIDENCE", "EMERGING_ENTITY")
    assert "Google Suggest" in result.methodology


def test_verify_ground_truth_api_endpoint():
    with _client() as client:
        payload = {
            "domain": "github.com",
            "brand": "GitHub",
            "keywords": ["software", "repositories"],
        }
        res = client.post("/api/v1/intelligence/verify/ground-truth", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["domain"] == "github.com"
        assert data["brand"] == "GitHub"
        assert "google_search_evidence" in data
        assert "wikidata_evidence" in data
        assert "duckduckgo_evidence" in data
        assert 0 <= data["overall_empirical_confidence"] <= 100

