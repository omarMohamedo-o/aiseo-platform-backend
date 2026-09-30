"""Google Gemini API adapter implementing the LlmProvider port."""

from __future__ import annotations

import json
from typing import TypeVar

import httpx
from pydantic import BaseModel

from ai.gateway.interfaces.text_model import LlmRequest, LlmResponse

T = TypeVar("T", bound=BaseModel)


class GeminiAdapter:
    """Adapter for Google Gemini models (e.g., gemini-1.5-pro)."""

    def __init__(
        self, api_key: str, default_model: str = "gemini-1.5-pro", timeout: float = 30.0
    ) -> None:
        self._api_key = api_key
        self._default_model = default_model
        self._timeout = timeout
        self._base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Free-form text generation using Gemini."""
        url = f"{self._base_url}/{self._default_model}:generateContent?key={self._api_key}"
        headers = {"Content-Type": "application/json"}

        payload = {
            "contents": [{"parts": [{"text": request.prompt}]}],
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }

        if request.system:
            payload["systemInstruction"] = {"parts": [{"text": request.system}]}

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            return LlmResponse(
                text=data["candidates"][0]["content"]["parts"][0]["text"],
                model=self._default_model,
                provider="gemini",
                input_tokens=data.get("usageMetadata", {}).get("promptTokenCount", 0),
                output_tokens=data.get("usageMetadata", {}).get("candidatesTokenCount", 0),
            )

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        """Structured generation using Gemini's JSON mode."""
        url = f"{self._base_url}/{self._default_model}:generateContent?key={self._api_key}"
        headers = {"Content-Type": "application/json"}

        # Convert JSON schema to Gemini Schema format (simple approximation)
        json_schema = schema.model_json_schema()

        payload = {
            "contents": [{"parts": [{"text": request.prompt}]}],
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
                "responseMimeType": "application/json",
                # Note: Full schema enforcement requires translating JSON schema to Gemini's
                # OpenAPI-like Schema format. For MVP, we rely on the mime-type and prompt.
            },
        }

        system_msg = request.system or "You are a helpful assistant."
        schema_str = json.dumps(json_schema)
        system_msg += f"\n\nYou MUST respond with valid JSON matching this schema: {schema_str}"

        payload["systemInstruction"] = {"parts": [{"text": system_msg}]}

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

            parsed = json.loads(raw_text)
            return schema(**parsed)
