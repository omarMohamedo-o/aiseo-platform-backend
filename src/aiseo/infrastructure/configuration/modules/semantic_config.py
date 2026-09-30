"""Configuration for text chunking, embeddings, and vector clustering."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChunkerConfig(BaseModel):
    """Recursive text chunking configuration."""

    chunk_size: int = Field(default=500, description="Maximum characters per chunk")
    chunk_overlap: int = Field(default=50, description="Overlapping characters between adjacent chunks")
    separators: list[str] = Field(
        default_factory=lambda: ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
        description="Priority order of separators for recursive chunking",
    )


class EmbeddingConfig(BaseModel):
    """Vector embeddings configuration."""

    provider: str = Field(default="openai", description="Embedding provider (e.g. openai, onnx)")
    model: str = Field(default="text-embedding-3-small", description="Embedding model name")
    dimensions: int = Field(default=1536, description="Embedding vector dimensions")


class ClusteringConfig(BaseModel):
    """Keyword & topic clustering configuration."""

    algorithm: str = Field(default="hdbscan", description="Clustering algorithm")
    min_cluster_size: int = Field(default=5, description="Minimum items per cluster")
