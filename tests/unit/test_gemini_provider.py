"""Unit tests for GeminiProvider adapter with mocked HTTP calls."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pydantic import BaseModel

from aiseo.adapters.llm.gemini_provider import GeminiProvider
from aiseo.domain.errors import (
    InvalidModelOutputError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
)
from aiseo.ports.llm.llm_provider import LlmRequest


class GeoMetrics(BaseModel):
    clarity_score: float
    brand_cited: bool


@pytest.mark.asyncio
async def test_gemini_generate_success() -> None:
    provider = GeminiProvider(api_key="test-gemini-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Gemini answer regarding brand presence."}],
                        "role": "model",
                    },
                    "finishReason": "STOP",
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 18,
                "candidatesTokenCount": 9,
                "totalTokenCount": 27,
            },
        },
        request=httpx.Request("POST", "https://mock.url"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Does AI cite our company?")
        res = await provider.generate(req)

        assert res.text == "Gemini answer regarding brand presence."
        assert res.provider == "gemini"
        assert res.input_tokens == 18
        assert res.output_tokens == 9


@pytest.mark.asyncio
async def test_gemini_generate_structured_success() -> None:
    provider = GeminiProvider(api_key="test-gemini-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": '{"clarity_score": 88.5, "brand_cited": true}'}
                        ],
                        "role": "model",
                    }
                }
            ]
        },
        request=httpx.Request("POST", "https://mock.url"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Evaluate GEO metrics.")
        result = await provider.generate_structured(req, GeoMetrics)

        assert isinstance(result, GeoMetrics)
        assert result.clarity_score == 88.5
        assert result.brand_cited is True


@pytest.mark.asyncio
async def test_gemini_structured_invalid_schema_raises_error() -> None:
    provider = GeminiProvider(api_key="test-gemini-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Not valid JSON for GeoMetrics"}],
                    }
                }
            ]
        },
        request=httpx.Request("POST", "https://mock.url"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Evaluate GEO metrics.")
        with pytest.raises(InvalidModelOutputError):
            await provider.generate_structured(req, GeoMetrics)


@pytest.mark.asyncio
async def test_gemini_resource_exhausted_maps_to_rate_limit() -> None:
    provider = GeminiProvider(api_key="test-gemini-key")

    mock_resp = httpx.Response(
        status_code=429,
        text="RESOURCE_EXHAUSTED: quota exceeded",
        request=httpx.Request("POST", "https://mock.url"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="test")
        with pytest.raises(ProviderRateLimitError):
            await provider.generate(req)


@pytest.mark.asyncio
async def test_gemini_auth_error_mapping() -> None:
    provider = GeminiProvider(api_key="bad-key")

    mock_resp = httpx.Response(
        status_code=403,
        text="API key not valid",
        request=httpx.Request("POST", "https://mock.url"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="test")
        with pytest.raises(ProviderAuthenticationError):
            await provider.generate(req)
