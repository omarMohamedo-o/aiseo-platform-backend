"""Integration tests for Reports, Opportunity Scoring, and Schedules API."""
import uuid

from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_generate_keyword_summary_with_scores() -> None:
    with _client() as client:
        tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"
        payload = {
            "keywords": [
                {
                    "keyword": "generative engine optimization",
                    "intent": "Informational",
                    "volume": "1,300",
                    "difficulty": 63,
                    "cpc": "$5.54",
                    "serp_features": 7,
                },
                {
                    "keyword": "seo vs geo",
                    "intent": "Commercial",
                    "volume": "40,500",
                    "difficulty": 94,
                    "cpc": "$7.89",
                    "serp_features": 8,
                },
            ],
            "tone": "executive",
        }

        response = client.post(
            "/api/v1/reports/summary",
            json=payload,
            headers={"X-Tenant-Id": tenant_id},
        )
        assert response.status_code == 200
        data = response.json()

        # Check summary narrative
        assert "summary" in data
        assert "headline" in data["summary"]
        assert "insights" in data["summary"]
        assert "actions" in data["summary"]

        # Check computed opportunity scores
        assert "scores" in data
        assert len(data["scores"]) == 2
        for s in data["scores"]:
            assert 0 <= s["score"] <= 100
            assert "keyword" in s


def test_branding_get_and_save() -> None:
    with _client() as client:
        tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"

        # 1. Get default branding
        get_res = client.get(
            "/api/v1/reports/branding",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert get_res.status_code == 200
        branding = get_res.json()
        assert "company_name" in branding

        # 2. Save customized branding
        branding_payload = {
            "company_name": "Acme Visibility Corp",
            "logo_url": "https://acme.com/logo.png",
            "primary_color": "#10b981",
            "accent_color": "#6366f1",
            "support_email": "reports@acme.com",
            "footer_text": "Confidential Executive Digest",
        }
        post_res = client.post(
            "/api/v1/reports/branding",
            json=branding_payload,
            headers={"X-Tenant-Id": tenant_id},
        )
        assert post_res.status_code == 200
        saved = post_res.json()
        assert saved["company_name"] == "Acme Visibility Corp"
        assert saved["accent_color"] == "#6366f1"


def test_schedules_crud_lifecycle() -> None:
    with _client() as client:
        tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"

        # 1. Create a scheduled report
        schedule_payload = {
            "name": "Weekly Monday Executive Digest",
            "cron": "0 9 * * 1",
            "recipient_email": "cmo@acme.com",
            "tone": "executive",
            "keywords": [
                {
                    "keyword": "ai search optimization",
                    "intent": "Commercial",
                    "volume": "12,000",
                    "difficulty": 45,
                    "cpc": "$6.20",
                    "serp_features": 6,
                }
            ],
        }

        create_res = client.post(
            "/api/v1/reports/schedules",
            json=schedule_payload,
            headers={"X-Tenant-Id": tenant_id},
        )
        assert create_res.status_code == 200
        created = create_res.json()
        schedule_id = created["id"]
        assert created["name"] == "Weekly Monday Executive Digest"
        assert created["recipient_email"] == "cmo@acme.com"

        # 2. List schedules
        list_res = client.get(
            "/api/v1/reports/schedules",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert list_res.status_code == 200
        items = list_res.json()
        assert any(item["id"] == schedule_id for item in items)

        # 3. Delete schedule
        del_res = client.delete(
            f"/api/v1/reports/schedules/{schedule_id}",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert del_res.status_code == 200
        assert del_res.json()["success"] is True

        # 4. Verify schedule removed
        list_after = client.get(
            "/api/v1/reports/schedules",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert not any(item["id"] == schedule_id for item in list_after.json())


def test_send_test_email() -> None:
    from unittest.mock import AsyncMock, patch

    with patch(
        "aiseo.application.reporting.scheduled_reports.ScheduledReportsService.send_test_report",
        new=AsyncMock(return_value=True),
    ), _client() as client:
        tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"
        payload = {
            "recipient_email": "analyst@example.com",
            "tone": "technical",
            "keywords": [
                {
                    "keyword": "generative engine optimization",
                    "intent": "Informational",
                    "volume": "1,300",
                    "difficulty": 63,
                    "cpc": "$5.54",
                    "serp_features": 7,
                }
            ],
        }

        response = client.post(
            "/api/v1/reports/send-test",
            json=payload,
            headers={"X-Tenant-Id": tenant_id},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
