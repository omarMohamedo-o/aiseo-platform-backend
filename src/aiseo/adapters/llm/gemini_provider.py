"""Google Gemini LLM provider adapter using async HTTP client."""
from __future__ import annotations

import json
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from aiseo.domain.errors import (
    InvalidModelOutputError,
    ProviderAuthenticationError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from aiseo.infrastructure.resilience.circuit_breaker import CircuitBreaker
from aiseo.infrastructure.resilience.retry import retry_async
from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest, LlmResponse

T = TypeVar("T", bound=BaseModel)


class GeminiProvider(LlmProvider):
    """Concrete LLM adapter for Google Gemini REST API."""

    DEFAULT_BASE_URL: str = (
        "https://generativelanguage.googleapis.com/v1beta/models"
    )

    def __init__(
        self,
        api_key: str,
        default_model: str = "gemini-1.5-flash",
        base_url: str | None = None,
        timeout: float = 30.0,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        self.api_key = api_key
        self.default_model = default_model
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.circuit_breaker = circuit_breaker or CircuitBreaker(
            name="GeminiProvider", failure_threshold=5, recovery_timeout_seconds=30.0
        )

    def _build_url(self, model: str) -> str:
        return f"{self.base_url}/{model}:generateContent?key={self.api_key}"

    def _build_payload(
        self, request: LlmRequest, response_mime_type: str | None = None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": request.prompt}],
                }
            ],
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }

        if request.system:
            payload["system_instruction"] = {
                "parts": [{"text": request.system}]
            }

        if response_mime_type:
            payload["generationConfig"]["responseMimeType"] = response_mime_type

        return payload

    async def _send_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = self._build_url(self.default_model)

        async def _call() -> dict[str, Any]:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json=payload,
                    )
                except httpx.TimeoutException as exc:
                    raise ProviderTimeoutError(f"Gemini request timed out: {exc}") from exc
                except httpx.RequestError as exc:
                    raise ProviderUnavailableError(f"Gemini network error: {exc}") from exc

                if response.status_code in (401, 403):
                    raise ProviderAuthenticationError(
                        f"Gemini authentication failed: {response.text}"
                    )
                if response.status_code == 429:
                    raise ProviderRateLimitError(
                        f"Gemini rate limit exceeded: {response.text}"
                    )
                if response.status_code >= 500:
                    raise ProviderUnavailableError(
                        f"Gemini server error (HTTP {response.status_code}): {response.text}"
                    )
                if response.status_code != 200:
                    raise ProviderError(
                        f"Gemini request failed (HTTP {response.status_code}): {response.text}"
                    )

                data: dict[str, Any] = response.json()
                if "error" in data:
                    err_msg = str(data["error"])
                    if "RESOURCE_EXHAUSTED" in err_msg:
                        raise ProviderRateLimitError(f"Gemini resource exhausted: {err_msg}")
                    raise ProviderError(f"Gemini API error: {err_msg}")

                return data

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

    async def generate(self, request: LlmRequest) -> LlmResponse:
        payload = self._build_payload(request)
        data = await self._send_request(payload)

        try:
            candidate = data["candidates"][0]
            parts = candidate["content"]["parts"]
            text = "".join(part.get("text", "") for part in parts)
            usage = data.get("usageMetadata", {})
            return LlmResponse(
                text=text,
                model=self.default_model,
                provider="gemini",
                input_tokens=usage.get("promptTokenCount", 0),
                output_tokens=usage.get("candidatesTokenCount", 0),
            )
        except (KeyError, IndexError) as exc:
            raise InvalidModelOutputError(
                f"Malformed Gemini response structure: {data}"
            ) from exc

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        schema_json = json.dumps(schema.model_json_schema())
        system_instruction = (
            f"{request.system or ''}\n\n"
            f"You MUST respond ONLY with a valid JSON object matching this schema:\n{schema_json}"
        ).strip()

        structured_request = LlmRequest(
            prompt=request.prompt,
            system=system_instruction,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            prompt_version=request.prompt_version,
        )

        payload = self._build_payload(
            structured_request, response_mime_type="application/json"
        )
        data = await self._send_request(payload)

        try:
            candidate = data["candidates"][0]
            parts = candidate["content"]["parts"]
            raw_text = "".join(part.get("text", "") for part in parts)
        except (KeyError, IndexError) as exc:
            raise InvalidModelOutputError(
                f"Malformed Gemini response structure: {data}"
            ) from exc

        try:
            return schema.model_validate_json(raw_text)
        except (ValidationError, ValueError) as exc:
            raise InvalidModelOutputError(
                f"Gemini output did not match expected schema {schema.__name__}: {exc}. Output was: {raw_text!r}"
            ) from exc
