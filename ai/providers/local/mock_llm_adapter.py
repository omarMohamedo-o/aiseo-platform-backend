"""Mock LLM Adapter for testing the Recommendation Engine without API costs."""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from ai.gateway.interfaces.text_model import LlmRequest, LlmResponse

T = TypeVar("T", bound=BaseModel)


class MockLlmAdapter:
    """Mock implementation of LlmProvider for deterministic testing."""

    def __init__(self, model_name: str) -> None:
        self._model_name = model_name

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Return a simple dummy response."""
        return LlmResponse(
            text=f"[MOCK RESPONSE from {self._model_name}] Generated fix for prompt: {request.prompt[:20]}...",
            model=self._model_name,
            provider="mock",
            input_tokens=10,
            output_tokens=20,
        )

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        """Return a mock structured response matching the Pydantic schema."""

        # We look for a special hint in the prompt to return specific data
        # For our Recommendation Engine MVP, we just return dummy data
        if "meta_description" in request.prompt.lower():
            # Attempt to instantiate the schema with dummy data
            # This is a naive mock, a real mock would parse the schema fields
            data = {
                "after_value": "Discover the best enterprise CRM software designed for scaling startups. Book a demo today."
            }
            return schema(**data)

        elif "title" in request.prompt.lower():
            data = {"after_value": "Acme CRM | The Best CRM for Startups"}
            return schema(**data)

        # Generic fallback
        data = {"after_value": f"Mock generated value from {self._model_name}"}
        return schema(**data)
