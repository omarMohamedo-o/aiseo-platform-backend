"""Provider-independent embedding capability port.

Defined as a `Protocol`; adapters compose the vendor client privately.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    texts: list[str]
    content_hash: str | None = None


class EmbeddingResponse(BaseModel):
    provider: str
    model: str
    dimensions: int
    vectors: list[list[float]]


@runtime_checkable
class EmbeddingProvider(Protocol):
    @property
    def dimensions(self) -> int:
        """Providers are not assumed to share dimensionality."""
        ...

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse: ...
