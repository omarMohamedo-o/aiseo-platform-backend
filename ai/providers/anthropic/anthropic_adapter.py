"""Anthropic API adapter implementing the LlmProvider port."""

from __future__ import annotations

from typing import TypeVar

import httpx
from pydantic import BaseModel

from ai.gateway.interfaces.text_model import LlmRequest, LlmResponse

T = TypeVar("T", bound=BaseModel)


class AnthropicAdapter:
    """Adapter for Anthropic's Claude models (e.g., Claude 3.5 Sonnet)."""

    def __init__(
        self, api_key: str, default_model: str = "claude-3-5-sonnet-20240620", timeout: float = 30.0
    ) -> None:
        self._api_key = api_key
        self._default_model = default_model
        self._timeout = timeout
        self._base_url = "https://api.anthropic.com/v1/messages"
        self._anthropic_version = "2023-06-01"

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Free-form text generation using Claude."""

        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": self._anthropic_version,
            "content-type": "application/json",
        }

        payload = {
            "model": self._default_model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": [{"role": "user", "content": request.prompt}],
        }

        if request.system:
            payload["system"] = request.system

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                self._base_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            return LlmResponse(
                text=data["content"][0]["text"],
                model=data["model"],
                provider="anthropic",
                input_tokens=data["usage"]["input_tokens"],
                output_tokens=data["usage"]["output_tokens"],
            )

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        """Structured generation using Claude's tool use (function calling)."""
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": self._anthropic_version,
            "content-type": "application/json",
        }

        json_schema = schema.model_json_schema()

        # Create a tool definition that matches the Pydantic schema
        tool_definition = {
            "name": "generate_response",
            "description": "Generate structured output based on the user request.",
            "input_schema": {
                "type": "object",
                "properties": json_schema.get("properties", {}),
                "required": json_schema.get("required", []),
            },
        }

        payload = {
            "model": self._default_model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "tools": [tool_definition],
            "tool_choice": {"type": "tool", "name": "generate_response"},
            "messages": [{"role": "user", "content": request.prompt}],
        }

        if request.system:
            payload["system"] = request.system

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                self._base_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            # Extract the tool use input
            for block in data["content"]:
                if block["type"] == "tool_use" and block["name"] == "generate_response":
                    tool_input = block["input"]
                    return schema(**tool_input)

            raise ValueError(f"Model failed to use tool correctly. Response: {data}")
