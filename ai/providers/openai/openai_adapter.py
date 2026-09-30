"""OpenAI API adapter implementing the LlmProvider port."""

from __future__ import annotations

import json
from typing import TypeVar

import httpx
from pydantic import BaseModel

from ai.gateway.interfaces.text_model import LlmRequest, LlmResponse

T = TypeVar("T", bound=BaseModel)


class OpenAIAdapter:
    """Adapter for OpenAI models (e.g., gpt-4o)."""

    def __init__(self, api_key: str, default_model: str = "gpt-4o", timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._default_model = default_model
        self._timeout = timeout
        self._base_url = "https://api.openai.com/v1"

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Free-form text generation using OpenAI."""

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        payload = {
            "model": self._default_model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            return LlmResponse(
                text=data["choices"][0]["message"]["content"],
                model=data["model"],
                provider="openai",
                input_tokens=data["usage"]["prompt_tokens"],
                output_tokens=data["usage"]["completion_tokens"],
            )

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        """Structured generation using OpenAI's JSON mode."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        # Inject schema instruction into system prompt
        system_msg = request.system or "You are a helpful assistant."
        schema_json = json.dumps(schema.model_json_schema())
        system_msg += f"\n\nYou MUST respond with valid JSON matching this schema: {schema_json}"

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": request.prompt},
        ]

        payload = {
            "model": self._default_model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "response_format": {"type": "json_object"},
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            raw_text = data["choices"][0]["message"]["content"]

            # Parse and validate with Pydantic
            parsed = json.loads(raw_text)
            return schema(**parsed)
