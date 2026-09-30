"""Unit tests for in-memory vector store."""
from __future__ import annotations

import pytest

from aiseo.adapters.semantic.in_memory_vector_store import (
    InMemoryVectorStore,
    _cosine_similarity,
)
from aiseo.domain.semantic.chunk import VectorRecord


def test_cosine_similarity_basic() -> None:
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert _cosine_similarity(v1, v2) == 1.0

    v3 = [0.0, 1.0, 0.0]
    assert _cosine_similarity(v1, v3) == 0.0

    # Opposite vectors
    v4 = [-1.0, 0.0, 0.0]
    assert _cosine_similarity(v1, v4) == -1.0


@pytest.mark.asyncio
async def test_vector_store_upsert_and_search() -> None:
    store = InMemoryVectorStore()

    records = [
        VectorRecord(
            chunk_id="doc1:0",
            document_id="doc1",
            vector=[1.0, 0.0, 0.0],
            text="Text about SEO and ranking on search engines.",
            metadata={"category": "seo"},
        ),
        VectorRecord(
            chunk_id="doc1:1",
            document_id="doc1",
            vector=[0.0, 1.0, 0.0],
            text="Text about machine learning and models.",
            metadata={"category": "ml"},
        ),
        VectorRecord(
            chunk_id="doc2:0",
            document_id="doc2",
            vector=[0.9, 0.1, 0.0],
            text="Text about Google search visibility.",
            metadata={"category": "seo"},
        ),
    ]

    await store.upsert(records)
    assert store.count == 3

    # Query closest to SEO [1.0, 0.0, 0.0]
    results = await store.search(query_vector=[1.0, 0.0, 0.0], top_k=2)
    assert len(results) == 2
    assert results[0].chunk_id == "doc1:0"
    assert results[0].similarity == 1.0
    assert results[1].chunk_id == "doc2:0"

    # Search with metadata filter
    ml_results = await store.search(
        query_vector=[1.0, 1.0, 0.0],
        top_k=5,
        filter_metadata={"category": "ml"},
    )
    assert len(ml_results) == 1
    assert ml_results[0].chunk_id == "doc1:1"


@pytest.mark.asyncio
async def test_vector_store_delete_by_document() -> None:
    store = InMemoryVectorStore()
    await store.upsert([
        VectorRecord(
            chunk_id="doc1:0",
            document_id="doc1",
            vector=[1.0, 0.0],
            text="Doc 1 chunk",
        ),
        VectorRecord(
            chunk_id="doc2:0",
            document_id="doc2",
            vector=[0.0, 1.0],
            text="Doc 2 chunk",
        ),
    ])

    await store.delete_by_document("doc1")
    assert store.count == 1

    remaining = await store.search(query_vector=[1.0, 0.0], top_k=5)
    assert len(remaining) == 1
    assert remaining[0].document_id == "doc2"
