"""Unit tests for ResendEmailAdapter."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from aiseo.adapters.notifications.resend_email_adapter import ResendEmailAdapter
from aiseo.domain.errors import ProviderAuthenticationError, ProviderRateLimitError


@pytest.mark.asyncio
async def test_email_adapter_success() -> None:
    adapter = ResendEmailAdapter(api_key="re_12345678")

    mock_resp = httpx.Response(
        status_code=200,
        json={"id": "email_msg_123"},
        request=httpx.Request("POST", adapter.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        result = await adapter.send_email(
            to=["client@example.com"],
            subject="Weekly AI Visibility Brief",
            html="<h1>Report</h1>",
            text="Report plain text",
        )
        assert result is True
        assert mock_post.call_count == 1


@pytest.mark.asyncio
async def test_email_adapter_auth_error() -> None:
    adapter = ResendEmailAdapter(api_key="invalid_key")

    mock_resp = httpx.Response(
        status_code=401,
        text="Invalid API key",
        request=httpx.Request("POST", adapter.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with pytest.raises(ProviderAuthenticationError):
            await adapter.send_email(
                to=["client@example.com"],
                subject="Test",
                html="<p>Test</p>",
                text="Test",
            )


@pytest.mark.asyncio
async def test_email_adapter_rate_limit_error() -> None:
    adapter = ResendEmailAdapter(api_key="re_12345678")

    mock_resp = httpx.Response(
        status_code=429,
        text="Too many requests",
        request=httpx.Request("POST", adapter.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with pytest.raises(ProviderRateLimitError):
            await adapter.send_email(
                to=["client@example.com"],
                subject="Test",
                html="<p>Test</p>",
                text="Test",
            )
