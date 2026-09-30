"""In-memory vector store adapter with cosine similarity search."""
from __future__ import annotations

import math

from aiseo.domain.semantic.chunk import SearchResult, VectorRecord
from aiseo.ports.semantic.vector_store_port import VectorStorePort


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class InMemoryVectorStore(VectorStorePort):
    """In-memory vector store ideal for fast test fixtures, session RAG, and local verification."""

    def __init__(self) -> None:
        self._records: dict[str, VectorRecord] = {}

    async def upsert(self, records: list[VectorRecord]) -> None:
        for rec in records:
            self._records[rec.chunk_id] = rec

    async def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        min_similarity: float = 0.0,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        matches: list[SearchResult] = []

        for rec in self._records.values():
            if filter_metadata:
                match_filter = all(
                    rec.metadata.get(k) == v for k, v in filter_metadata.items()
                )
                if not match_filter:
                    continue

            similarity = _cosine_similarity(query_vector, rec.vector)
            if similarity >= min_similarity:
                matches.append(
                    SearchResult(
                        chunk_id=rec.chunk_id,
                        document_id=rec.document_id,
                        text=rec.text,
                        similarity=round(similarity, 4),
                        metadata=rec.metadata,
                    )
                )

        matches.sort(key=lambda x: x.similarity, reverse=True)
        return matches[:top_k]

    async def delete_by_document(self, document_id: str) -> None:
        to_delete = [
            cid for cid, rec in self._records.items() if rec.document_id == document_id
        ]
        for cid in to_delete:
            del self._records[cid]

    def clear(self) -> None:
        self._records.clear()

    @property
    def count(self) -> int:
        return len(self._records)
