"""Domain models for RAG faithfulness, citation grounding, and hallucination metrics."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GroundingStatus = Literal["GROUNDED", "PARTIALLY_GROUNDED", "HALLUCINATED", "UNVERIFIED"]


class HallucinationMetrics(BaseModel):
    """Factual grounding and hallucination metrics for an AI-generated answer."""

    model_config = ConfigDict(frozen=True)

    grounding_ratio: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Ratio of verified claims present in source context (0.0 to 1.0).",
    )
    hallucination_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Hallucination severity index (0.0 = fully grounded, 1.0 = completely hallucinated).",
    )
    is_hallucinated: bool = Field(
        default=False,
        description="True if hallucination score exceeds the risk threshold (default > 0.45).",
    )
    status: GroundingStatus = Field(
        default="GROUNDED",
        description="Categorical grounding classification.",
    )
    verified_claims: list[str] = Field(
        default_factory=list,
        description="Claims and attributes validated against the crawled website.",
    )
    unverified_claims: list[str] = Field(
        default_factory=list,
        description="Claims present in the AI response but missing or contradictory in source context.",
    )
    cited_references: list[str] = Field(
        default_factory=list,
        description="Extracted domain and citation references.",
    )
