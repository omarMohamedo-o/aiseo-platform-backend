import uuid

from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_health_check() -> None:
    with _client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_register_website_returns_201_and_dto() -> None:
    with _client() as client:
        tenant_id = str(uuid.uuid4())
        response = client.post(
            "/api/v1/websites",
            json={"url": "https://example.com"},
            headers={"X-Tenant-Id": tenant_id},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["url"] == "https://example.com"
        assert body["status"] == "REGISTERED"


def test_register_website_rejects_invalid_url() -> None:
    with _client() as client:
        response = client.post(
            "/api/v1/websites",
            json={"url": "not-a-url"},
            headers={"X-Tenant-Id": str(uuid.uuid4())},
        )
        assert response.status_code == 422


def test_register_website_requires_tenant_header() -> None:
    with _client() as client:
        response = client.post("/api/v1/websites", json={"url": "https://example.com"})
        assert response.status_code == 422  # missing required header


def test_crawl_and_analyze_endpoint_structure() -> None:
    with _client() as client:
        response = client.post(
            "/api/v1/websites/crawl-and-analyze",
            json={"url": "https://example.com", "brand_name": "ExampleCorp", "max_pages": 2},
        )
        assert response.status_code in (200, 502)
        if response.status_code == 200:
            body = response.json()
            assert body["brand_name"] == "ExampleCorp"
            assert "discovered_pages" in body
            assert "raw_text_snippet" in body
            assert "opportunity_score" in body
            assert "visibility_score" in body
