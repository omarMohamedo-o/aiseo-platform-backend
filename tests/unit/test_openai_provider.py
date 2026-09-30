"""Unit tests for OpenAiProvider adapter with mocked HTTP calls."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pydantic import BaseModel

from aiseo.adapters.llm.openai_provider import OpenAiProvider
from aiseo.domain.errors import (
    InvalidModelOutputError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
)
from aiseo.ports.llm.llm_provider import LlmRequest


class SampleSchema(BaseModel):
    summary: str
    confidence: float


@pytest.mark.asyncio
async def test_openai_generate_success() -> None:
    provider = OpenAiProvider(api_key="test-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "id": "chatcmpl-123",
            "model": "gpt-4o-mini",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Search engines index websites."},
                }
            ],
            "usage": {"prompt_tokens": 12, "completion_tokens": 8},
        },
        request=httpx.Request("POST", provider.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Explain SEO in one sentence.")
        res = await provider.generate(req)

        assert res.text == "Search engines index websites."
        assert res.provider == "openai"
        assert res.input_tokens == 12
        assert res.output_tokens == 8


@pytest.mark.asyncio
async def test_openai_generate_structured_success() -> None:
    provider = OpenAiProvider(api_key="test-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "choices": [
                {
                    "message": {
                        "content": '{"summary": "High visibility on Google", "confidence": 0.95}'
                    }
                }
            ],
            "usage": {"prompt_tokens": 20, "completion_tokens": 15},
        },
        request=httpx.Request("POST", provider.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Evaluate visibility.")
        structured_obj = await provider.generate_structured(req, SampleSchema)

        assert isinstance(structured_obj, SampleSchema)
        assert structured_obj.summary == "High visibility on Google"
        assert structured_obj.confidence == 0.95


@pytest.mark.asyncio
async def test_openai_structured_invalid_json_raises_domain_error() -> None:
    provider = OpenAiProvider(api_key="test-key")

    mock_resp = httpx.Response(
        status_code=200,
        json={
            "choices": [
                {
                    "message": {
                        "content": "Not valid JSON output here"
                    }
                }
            ],
        },
        request=httpx.Request("POST", provider.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="Evaluate visibility.")
        with pytest.raises(InvalidModelOutputError):
            await provider.generate_structured(req, SampleSchema)


@pytest.mark.asyncio
async def test_openai_rate_limit_error_mapping() -> None:
    provider = OpenAiProvider(api_key="test-key")

    mock_resp = httpx.Response(
        status_code=429,
        text="Rate limit reached for requests per minute",
        request=httpx.Request("POST", provider.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="test")
        with pytest.raises(ProviderRateLimitError):
            await provider.generate(req)


@pytest.mark.asyncio
async def test_openai_auth_error_mapping() -> None:
    provider = OpenAiProvider(api_key="bad-key")

    mock_resp = httpx.Response(
        status_code=401,
        text="Incorrect API key provided",
        request=httpx.Request("POST", provider.api_url),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        req = LlmRequest(prompt="test")
        with pytest.raises(ProviderAuthenticationError):
            await provider.generate(req)
