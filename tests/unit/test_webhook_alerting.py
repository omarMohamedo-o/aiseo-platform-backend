"""Unit tests for Webhook Incident Alerting Adapter.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import hmac
import hashlib
import json
import pytest
import httpx

from aiseo.adapters.notifications.webhook_adapter import WebhookAlertAdapter
from aiseo.ports.notifications.webhook_port import WebhookAlert
from tests.test_config import (
    TARGET_DOMAIN,
    TEST_CONFIG,
)


@pytest.mark.asyncio
async def test_webhook_dispatches_successfully() -> None:
    captured_requests: list[httpx.Request] = []

    def mock_transport(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        return httpx.Response(200, json={"status": "ok"})

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_transport))
    adapter = WebhookAlertAdapter(
        webhook_url=TEST_CONFIG.alerts.webhook_url,
        secret_key=TEST_CONFIG.alerts.secret_key,
        rate_limit_seconds=TEST_CONFIG.alerts.rate_limit_seconds,
        client=client,
    )

    alert = WebhookAlert(
        domain=TARGET_DOMAIN,
        alert_type="HIGH_HALLUCINATION",
        severity="critical",
        message="Brand hallucination spiked to 0.45 in ChatGPT queries.",
        details={"hallucination_score": 0.45, "unverified_claims": 3},
    )

    success = await adapter.send_alert(alert)
    assert success is True
    assert len(captured_requests) == 1

    req = captured_requests[0]
    body = json.loads(req.content.decode("utf-8"))
    assert body["domain"] == TARGET_DOMAIN
    assert body["alert_type"] == "HIGH_HALLUCINATION"
    assert body["severity"] == "critical"

    # Verify HMAC-SHA256 signature
    sig = req.headers.get("X-AISEO-Signature")
    assert sig is not None
    expected_sig = hmac.new(TEST_CONFIG.alerts.secret_key.encode("utf-8"), req.content, hashlib.sha256).hexdigest()
    assert sig == expected_sig


@pytest.mark.asyncio
async def test_webhook_storm_rate_limiting() -> None:
    captured_count = 0

    def mock_transport(request: httpx.Request) -> httpx.Response:
        nonlocal captured_count
        captured_count += 1
        return httpx.Response(200, json={"status": "ok"})

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_transport))
    adapter = WebhookAlertAdapter(
        webhook_url="https://hooks.enterprise.com/alerts",
        rate_limit_seconds=10.0,
        client=client,
    )

    alert = WebhookAlert(
        domain=TARGET_DOMAIN,
        alert_type="VISIBILITY_DROP",
        severity="warning",
        message="Visibility dropped 10%.",
    )

    # First dispatch should succeed
    res1 = await adapter.send_alert(alert)
    assert res1 is True
    assert captured_count == 1

    # Second dispatch within 10s window must be suppressed
    res2 = await adapter.send_alert(alert)
    assert res2 is False
    assert captured_count == 1

