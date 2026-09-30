"""Provider-independent LLM capability port.

Defined as a `Protocol`: vendor adapters (OpenAI, Anthropic, Gemini, ...)
implement this structurally, composing the vendor SDK client as a private
attribute, rather than inheriting from a shared base class.
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LlmRequest(BaseModel):
    prompt: str
    system: str | None = None
    temperature: float = 0.0
    max_tokens: int = 1024
    prompt_version: str | None = None


class LlmResponse(BaseModel):
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int


@runtime_checkable
class LlmProvider(Protocol):
    """Capability-specific interface. Business code depends only on this,
    never on a concrete vendor SDK."""

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Free-form text generation."""
        ...

    async def generate_structured(self, request: LlmRequest, schema: type[T]) -> T:
        """Structured, schema-validated generation for business-critical output.

        Implementations must validate the model output against `schema` and
        raise `InvalidModelOutputError` (translated at the adapter boundary)
        on malformed output rather than returning free-form prose.
        """
        ...


class SupportsLlmCapability(Protocol):
    """Marker protocol used by the capability model / provider registry."""

    def supports_llm(self) -> bool: ...
