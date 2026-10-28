"""Domain models for AI answer analysis and visibility scoring."""
from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field

SentimentType = Literal["positive", "neutral", "negative", "mixed"]


class Citation(BaseModel):
    """Citation URL extracted from an AI response."""

    model_config = ConfigDict(frozen=True)

    url: str
    domain: str

    @classmethod
    def from_url(cls, raw_url: str) -> Citation:
        parsed = urlparse(raw_url)
        return cls(url=raw_url, domain=parsed.netloc or raw_url)


class BrandMention(BaseModel):
    """Detected mention of a target brand in an AI response."""

    model_config = ConfigDict(frozen=True)

    brand_name: str
    mentioned: bool
    position: int | None = None
    sentiment: SentimentType = "neutral"


class AnswerAnalysisResult(BaseModel):
    """Normalized evidence record from analyzing a single AI model's response."""

    model_config = ConfigDict(frozen=True)

    prompt_run_id: str
    provider: str  # e.g., "openai", "gemini", "claude", "perplexity"
    question: str
    brand: str
    brand_mentioned: bool
    mention_position: int | None = None
    competitors: list[str] = Field(default_factory=list)
    extracted_citations: list[str] = Field(default_factory=list)
    sentiment: SentimentType = "neutral"
    visibility_score: int = Field(ge=0, le=100)
    summary: str
    analysis_model: str = "deterministic"
    # Factual grounding & hallucination metrics (Stage A)
    hallucination_score: float = Field(default=0.0, ge=0.0, le=1.0)
    faithfulness_ratio: float = Field(default=1.0, ge=0.0, le=1.0)
    grounding_status: str = "GROUNDED"
    unverified_claims: list[str] = Field(default_factory=list)
