"""Semantic domain models: chunks, documents, and vector search representations."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TextChunk(BaseModel):
    """An individual piece of partitioned text with positional and contextual metadata."""

    model_config = ConfigDict(frozen=True)

    id: str
    document_id: str
    text: str
    sequence: int
    char_count: int = Field(default=0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create(
        cls,
        document_id: str,
        text: str,
        sequence: int,
        metadata: dict[str, Any] | None = None,
    ) -> TextChunk:
        chunk_id = f"{document_id}:{sequence}"
        meta = metadata.copy() if metadata else {}
        meta["sequence"] = str(sequence)
        return cls(
            id=chunk_id,
            document_id=document_id,
            text=text,
            sequence=sequence,
            char_count=len(text),
            metadata=meta,
        )


class VectorRecord(BaseModel):
    """A vector embedding coupled with its source chunk and metadata."""

    model_config = ConfigDict(frozen=True)

    chunk_id: str
    document_id: str
    vector: list[float]
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """Vector similarity search match result."""

    model_config = ConfigDict(frozen=True)

    chunk_id: str
    document_id: str
    text: str
    similarity: float
    metadata: dict[str, Any] = Field(default_factory=dict)
