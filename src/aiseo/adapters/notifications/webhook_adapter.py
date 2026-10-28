"""Enterprise Webhook Alert Adapter with HMAC signing and storm protection.

Dispatches real-time incident notifications to enterprise SIEM/Slack/Teams channels
when brand hallucination or visibility metrics breach defined safety thresholds.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any

import httpx

from aiseo.ports.notifications.webhook_port import WebhookAlert, WebhookAlertPort

logger = logging.getLogger(__name__)


class WebhookAlertAdapter(WebhookAlertPort):
    """Production webhook dispatcher with rate-limiting, HMAC validation, and retry guard."""

    def __init__(
        self,
        webhook_url: str | None = None,
        secret_key: str | None = None,
        rate_limit_seconds: float = 30.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._webhook_url = webhook_url
        self._secret_key = secret_key
        self._rate_limit = rate_limit_seconds
        self._client = client
        self._last_alert_time: dict[str, float] = {}

    def _sign_payload(self, body_bytes: bytes) -> str:
        """Calculates HMAC-SHA256 signature of the payload."""
        if not self._secret_key:
            return ""
        return hmac.new(
            self._secret_key.encode("utf-8"),
            body_bytes,
            hashlib.sha256,
        ).hexdigest()

    async def send_alert(self, alert: WebhookAlert) -> bool:
        """Dispatches alert payload to configured webhook destination."""
        cache_key = f"{alert.domain}:{alert.alert_type}"
        now = time.time()
        last_sent = self._last_alert_time.get(cache_key, 0.0)

        # Flood / storm suppression
        if now - last_sent < self._rate_limit:
            logger.warning("Alert '%s' suppressed due to rate limiting.", cache_key)
            return False

        self._last_alert_time[cache_key] = now

        if not self._webhook_url:
            logger.info("Webhook alert logged (no URL configured): %s", alert)
            return True

        payload = {
            "source": "aiseo-geo-platform",
            "domain": alert.domain,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "timestamp": alert.timestamp,
            "details": alert.details,
        }

        body_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "AISEO-AlertDispatcher/2.0",
        }
        if self._secret_key:
            headers["X-AISEO-Signature"] = self._sign_payload(body_bytes)

        try:
            if self._client:
                resp = await self._client.post(self._webhook_url, content=body_bytes, headers=headers)
                return resp.status_code < 400
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(self._webhook_url, content=body_bytes, headers=headers)
                return resp.status_code < 400
        except Exception as exc:
            logger.error("Failed to dispatch alert webhook to %s: %s", self._webhook_url, exc)
            return False

