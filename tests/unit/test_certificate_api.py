"""Unit tests for the official GEO Compliance Certificate generation & verification API."""
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings
from tests.test_config import TARGET_DOMAIN


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_issue_certificate_endpoint():
    with _client() as client:
        payload = {
            "domain": "acme-corp.com",
            "brand_name": "Acme Global",
            "visibility_score": 92,
            "grounding_score": 98,
            "schema_score": 100,
        }
        res = client.post("/api/v1/reports/certificate/issue", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["certificate_id"].startswith("GEO-CERT-2026-")
        assert data["domain"] == "acme-corp.com"
        assert data["brand_name"] == "Acme Global"
        assert data["certification_tier"] == "Platinum Enterprise"
        assert len(data["verification_hash"]) == 32
        assert data["lead_architect"] == "Omar Mohamed (@omarMohamedo-o)"
        assert "Copyright © 2026 Omar Mohamed" in data["copyright_notice"]


def test_get_domain_certificate_endpoint():
    with _client() as client:
        res = client.get(f"/api/v1/reports/certificate/{TARGET_DOMAIN}")
        assert res.status_code == 200
        data = res.json()
        assert data["domain"] == TARGET_DOMAIN
        assert data["status"] == "VALID"
        assert data["issuer"] == "AISEO Platform Global Standards Board"
        assert data["visibility_score"] >= 0

