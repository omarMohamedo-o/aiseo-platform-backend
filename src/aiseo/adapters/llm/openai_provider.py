"""OpenAI LLM provider adapter using async HTTP client."""
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


class OpenAiProvider(LlmProvider):
    """Concrete LLM adapter for OpenAI chat completions API."""

    DEFAULT_API_URL: str = "https://api.openai.com/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        default_model: str = "gpt-4o-mini",
        api_url: str | None = None,
        timeout: float = 30.0,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        self.api_key = api_key
        self.default_model = default_model
        self.api_url = api_url or self.DEFAULT_API_URL
        self.timeout = timeout
        self.circuit_breaker = circuit_breaker or CircuitBreaker(
            name="OpenAiProvider", failure_threshold=5, recovery_timeout_seconds=30.0
        )

    def _build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _build_messages(self, request: LlmRequest) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    async def _send_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        clean_key = self.api_key.strip() if self.api_key else ""
        if not clean_key or clean_key.startswith("mock"):
            raise ProviderAuthenticationError("OpenAI API key is unconfigured or mock.")

        async def _call() -> dict[str, Any]:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.post(
                        self.api_url,
                        headers=self._build_headers(),
                        json=payload,
                    )
                except httpx.TimeoutException as exc:
                    raise ProviderTimeoutError(f"OpenAI request timed out: {exc}") from exc
                except httpx.RequestError as exc:
                    raise ProviderUnavailableError(f"OpenAI network error: {exc}") from exc

                if response.status_code in (401, 403):
                    raise ProviderAuthenticationError(
                        f"OpenAI authentication failed: {response.text}"
                    )
                if response.status_code == 429:
                    raise ProviderRateLimitError(
                        f"OpenAI rate limit exceeded: {response.text}"
                    )
                if response.status_code >= 500:
                    raise ProviderUnavailableError(
                        f"OpenAI server error (HTTP {response.status_code}): {response.text}"
                    )
                if response.status_code != 200:
                    raise ProviderError(
                        f"OpenAI request failed (HTTP {response.status_code}): {response.text}"
                    )

                return response.json()  # type: ignore[no-any-return]

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
        payload = {
            "model": self.default_model,
            "messages": self._build_messages(request),
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        data = await self._send_request(payload)

        try:
            choice = data["choices"][0]
            text = choice["message"]["content"]
            usage = data.get("usage", {})
            return LlmResponse(
                text=text,
                model=data.get("model", self.default_model),
                provider="openai",
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
            )
        except (KeyError, IndexError) as exc:
            raise InvalidModelOutputError(
                f"Malformed OpenAI response structure: {data}"
            ) from exc

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        schema_json = json.dumps(schema.model_json_schema())
        system_instruction = (
            f"{request.system or ''}\n\n"
            f"You MUST respond ONLY with a valid JSON object strictly matching this JSON schema:\n{schema_json}"
        ).strip()

        structured_request = LlmRequest(
            prompt=request.prompt,
            system=system_instruction,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            prompt_version=request.prompt_version,
        )

        payload = {
            "model": self.default_model,
            "messages": self._build_messages(structured_request),
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "response_format": {"type": "json_object"},
        }

        data = await self._send_request(payload)

        try:
            choice = data["choices"][0]
            raw_text = choice["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise InvalidModelOutputError(
                f"Malformed OpenAI response structure: {data}"
            ) from exc

        try:
            return schema.model_validate_json(raw_text)
        except (ValidationError, ValueError) as exc:
            raise InvalidModelOutputError(
                f"Model output did not match expected schema {schema.__name__}: {exc}. Output was: {raw_text!r}"
            ) from exc
