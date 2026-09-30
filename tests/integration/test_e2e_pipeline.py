"""End-to-End multi-stage pipeline integration test."""
import uuid

from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_full_platform_pipeline_e2e() -> None:
    """Simulates a complete enterprise customer onboarding and audit pipeline:

    1. Store encrypted API credentials in tenant vault
    2. Register company website
    3. Crawl, extract text, chunk, and score opportunity
    4. Generate strategic buyer persona questions
    5. Audit citations and brand mentions across models
    6. Generate executive report summary
    7. Provision white-label branding and automated email schedule
    """
    with _client() as client:
        tenant_id = str(uuid.uuid4())
        headers = {"X-Tenant-Id": tenant_id}

        # Step 1: Store encrypted credentials in Vault
        vault_res = client.post(
            "/api/v1/vault/credentials",
            json={
                "provider": "openai",
                "api_url": "https://api.openai.com/v1",
                "api_key": "sk-proj-live-mock-vault-key-99999",
                "model": "gpt-4o",
            },
            headers=headers,
        )
        assert vault_res.status_code == 200
        assert vault_res.json()["success"] is True

        # Step 2: Register company website
        reg_res = client.post(
            "/api/v1/websites",
            json={"url": "https://example.com"},
            headers=headers,
        )
        assert reg_res.status_code == 201
        assert reg_res.json()["url"] == "https://example.com"
        assert reg_res.json()["status"] == "REGISTERED"

        # Step 3: Crawl and Analyze live website
        crawl_res = client.post(
            "/api/v1/websites/crawl-and-analyze",
            json={
                "url": "https://example.com",
                "brand_name": "ExampleCorp",
                "max_pages": 2,
            },
            headers=headers,
        )
        assert crawl_res.status_code in (200, 502)
        if crawl_res.status_code == 200:
            crawl_data = crawl_res.json()
            assert crawl_data["brand_name"] == "ExampleCorp"
            assert "discovered_pages" in crawl_data
            assert "sample_chunks" in crawl_data
            assert 0 <= crawl_data["opportunity_score"] <= 100

        # Step 4: Generate Question Set for buyer personas
        q_res = client.post(
            "/api/v1/intelligence/questions/generate",
            json={
                "topic": "ExampleCorp Enterprise Analytics",
                "keywords": ["ExampleCorp", "analytics", "reporting"],
                "lens": "geo",
                "count": 3,
            },
            headers=headers,
        )
        assert q_res.status_code == 200
        q_data = q_res.json()
        assert len(q_data["questions"]) > 0

        # Step 5: Answer Analysis & Citation Auditing
        analysis_res = client.post(
            "/api/v1/visibility/answers/analyze",
            json={
                "brand": "ExampleCorp",
                "items": [
                    {
                        "prompt_run_id": "e2e-run-1",
                        "provider": "perplexity",
                        "question": "What is ExampleCorp?",
                        "answer": "ExampleCorp provides enterprise solutions. Reference: https://example.com",
                        "citations": ["https://example.com"],
                    }
                ],
            },
            headers=headers,
        )
        assert analysis_res.status_code == 200
        analysis_data = analysis_res.json()
        assert len(analysis_data) == 1
        assert analysis_data[0]["brand_mentioned"] is True
        assert "https://example.com" in analysis_data[0]["extracted_citations"]

        # Step 6: Generate Executive Report Summary
        report_res = client.post(
            "/api/v1/reports/summary",
            json={
                "keywords": [
                    {
                        "keyword": "enterprise analytics",
                        "intent": "Commercial",
                        "volume": "18,500",
                        "difficulty": 52,
                        "cpc": "$8.20",
                        "serp_features": 6,
                    }
                ],
                "tone": "executive",
            },
            headers=headers,
        )
        assert report_res.status_code == 200
        report_data = report_res.json()
        assert "summary" in report_data
        assert len(report_data["scores"]) == 1

        # Step 7: Configure White-Label Branding & Email Schedule
        brand_res = client.post(
            "/api/v1/reports/branding",
            json={
                "company_name": "ExampleCorp Global",
                "logo_url": "https://example.com/logo.svg",
                "accent_color": "#38bdf8",
                "footer_text": "Confidential Intelligence",
            },
            headers=headers,
        )
        assert brand_res.status_code == 200

        schedule_res = client.post(
            "/api/v1/reports/schedules",
            json={
                "name": "Weekly Monday Executive Digest",
                "cron": "0 9 * * 1",
                "recipient_email": "leadership@example.com",
                "tone": "executive",
                "keywords": [
                    {
                        "keyword": "enterprise analytics",
                        "intent": "Commercial",
                        "volume": "18,500",
                        "difficulty": 52,
                        "cpc": "$8.20",
                        "serp_features": 6,
                    }
                ],
            },
            headers=headers,
        )
        assert schedule_res.status_code == 200
        schedule_id = schedule_res.json()["id"]

        # Verify schedule exists in listing
        schedules_list = client.get("/api/v1/reports/schedules", headers=headers)
        assert any(s["id"] == schedule_id for s in schedules_list.json())
