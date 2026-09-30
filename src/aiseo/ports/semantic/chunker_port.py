"""Chunker capability port."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from aiseo.domain.semantic.chunk import TextChunk


@runtime_checkable
class ChunkerPort(Protocol):
    """Protocol for partitioning text into chunks."""

    def chunk(
        self,
        document_id: str,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        metadata: dict[str, Any] | None = None,
    ) -> list[TextChunk]:
        """Split document text into a sequence of TextChunk objects."""
        ...
