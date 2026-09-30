"""Resend-compatible email notification adapter."""
from __future__ import annotations

import logging
from typing import Any

import httpx

from aiseo.domain.errors import (
    ProviderAuthenticationError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from aiseo.infrastructure.resilience.circuit_breaker import CircuitBreaker
from aiseo.infrastructure.resilience.retry import retry_async
from aiseo.ports.notifications.email_port import EmailPort

logger = logging.getLogger(__name__)


class ResendEmailAdapter(EmailPort):
    """Concrete adapter for delivering scheduled and alert reports via Resend / REST email API."""

    DEFAULT_API_URL: str = "https://api.resend.com/emails"
    DEFAULT_FROM_SENDER: str = "SignalOS Reports <reports@signalos.ai>"

    def __init__(
        self,
        api_key: str,
        api_url: str | None = None,
        default_sender: str | None = None,
        timeout: float = 15.0,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url or self.DEFAULT_API_URL
        self.default_sender = default_sender or self.DEFAULT_FROM_SENDER
        self.timeout = timeout
        self.circuit_breaker = circuit_breaker or CircuitBreaker(
            name="ResendEmailAdapter", failure_threshold=5, recovery_timeout_seconds=30.0
        )

    async def send_email(
        self,
        to: list[str],
        subject: str,
        html: str,
        text: str,
        from_sender: str | None = None,
    ) -> bool:
        if not to:
            raise ValueError("Recipient email list 'to' must not be empty.")

        sender = from_sender or self.default_sender
        payload: dict[str, Any] = {
            "from": sender,
            "to": to,
            "subject": subject,
            "html": html,
            "text": text,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async def _call() -> bool:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.post(
                        self.api_url,
                        headers=headers,
                        json=payload,
                    )
                except httpx.TimeoutException as exc:
                    raise ProviderTimeoutError(f"Email delivery timed out: {exc}") from exc
                except httpx.RequestError as exc:
                    raise ProviderUnavailableError(f"Email delivery network error: {exc}") from exc

                if response.status_code in (401, 403):
                    raise ProviderAuthenticationError(
                        f"Email API authentication failed: {response.text}"
                    )
                if response.status_code == 429:
                    raise ProviderRateLimitError(
                        f"Email API rate limit exceeded: {response.text}"
                    )
                if response.status_code >= 500:
                    raise ProviderUnavailableError(
                        f"Email API server error (HTTP {response.status_code}): {response.text}"
                    )
                if response.status_code not in (200, 201, 202):
                    raise ProviderError(
                        f"Email delivery failed (HTTP {response.status_code}): {response.text}"
                    )

                logger.info(f"Report email successfully delivered to {to}: '{subject}'")
                return True

        return await self.circuit_breaker.execute(
            lambda: retry_async(
                _call,
                max_retries=2,
                initial_delay=0.5,
                retryable_exceptions=(
                    ProviderRateLimitError,
                    ProviderTimeoutError,
                    ProviderUnavailableError,
                ),
                non_retryable_exceptions=(
                    ProviderAuthenticationError,
                ),
            )
        )
