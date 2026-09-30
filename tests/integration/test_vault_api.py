"""Integration tests for Encrypted Security Vault API."""
import uuid

from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.configuration.settings import Settings


def _client() -> TestClient:
    app = create_app(settings=Settings())
    return TestClient(app)


def test_vault_credentials_lifecycle_and_masking() -> None:
    with _client() as client:
        tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"

        # 1. Initial status: all providers should be unconfigured
        status_res = client.get(
            "/api/v1/vault/status",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert status_res.status_code == 200
        statuses = status_res.json()
        assert len(statuses) >= 4
        openai_status = next(s for s in statuses if s["provider"] == "openai")
        assert openai_status["configured"] is False

        # 2. Save an encrypted credential
        save_payload = {
            "provider": "openai",
            "api_url": "https://api.openai.com/v1",
            "api_key": "sk-proj-super-secret-api-key-12345",
            "model": "gpt-4o",
        }
        save_res = client.post(
            "/api/v1/vault/credentials",
            json=save_payload,
            headers={"X-Tenant-Id": tenant_id},
        )
        assert save_res.status_code == 200
        assert save_res.json()["success"] is True

        # 3. Check status: should be configured, key MUST be masked (never returned in plaintext)
        status_after = client.get(
            "/api/v1/vault/status",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert status_after.status_code == 200
        openai_after = next(s for s in status_after.json() if s["provider"] == "openai")
        assert openai_after["configured"] is True
        assert openai_after["masked_key"] != "sk-proj-super-secret-api-key-12345"
        assert "••••••" in openai_after["masked_key"]

        # 4. Delete credential
        del_res = client.delete(
            "/api/v1/vault/credentials/openai",
            headers={"X-Tenant-Id": tenant_id},
        )
        assert del_res.status_code == 200
        assert del_res.json()["success"] is True

        # 5. Check status after deletion
        status_final = client.get(
            "/api/v1/vault/status",
            headers={"X-Tenant-Id": tenant_id},
        )
        openai_final = next(s for s in status_final.json() if s["provider"] == "openai")
        assert openai_final["configured"] is False


def test_vault_validates_key_minimum_length() -> None:
    with _client() as client:
        # Key too short (<6 characters)
        response = client.post(
            "/api/v1/vault/credentials",
            json={
                "provider": "anthropic",
                "api_url": "https://api.anthropic.com",
                "api_key": "short",
            },
            headers={"X-Tenant-Id": "test-tenant"},
        )
        assert response.status_code == 422
