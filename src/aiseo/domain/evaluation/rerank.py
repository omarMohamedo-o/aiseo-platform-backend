"""Domain models for Hybrid Search (BM25 + Vector) and Cross-Encoder Reranking."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RerankCandidate(BaseModel):
    """Candidate passage retrieved for a given query."""

    model_config = ConfigDict(frozen=True)

    text: str
    doc_id: str = "doc-0"
    chunk_index: int = 0
    lexical_bm25_score: float = 0.0
    dense_vector_score: float = 0.0
    rerank_score: float = 0.0
    final_score: float = 0.0


class SnippetPrediction(BaseModel):
    """Predicted 40-60 word answer snippet likely to be extracted by AI & Answer Engines."""

    model_config = ConfigDict(frozen=True)

    question: str
    predicted_snippet: str
    doc_id: str = "doc-0"
    confidence: float = Field(ge=0.0, le=1.0)
    word_count: int
    is_ideal_aeo_length: bool = Field(
        default=True,
        description="True if word count is in the 40-60 word Featured Snippet sweet spot.",
    )
    recommended_heading: str | None = None

