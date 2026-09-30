"""Vector store capability port."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from aiseo.domain.semantic.chunk import SearchResult, VectorRecord


@runtime_checkable
class VectorStorePort(Protocol):
    """Protocol for storing and performing similarity search on vector embeddings."""

    async def upsert(self, records: list[VectorRecord]) -> None:
        """Insert or update embedding records."""
        ...

    async def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        min_similarity: float = 0.0,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        """Perform cosine similarity nearest neighbor search."""
        ...

    async def delete_by_document(self, document_id: str) -> None:
        """Delete all vectors associated with a document."""
        ...
