"""Domain models for Generative Engine Optimization (GEO) Simulations."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BrandMention(BaseModel):
    """Represents a detected mention of the client's brand in an AI response."""

    brand_name: str
    mentioned: bool
    sentiment: Literal["POSITIVE", "NEGATIVE", "NEUTRAL", "NONE"] = "NONE"
    rank_position: int | None = None  # e.g., if it says "1. Acme, 2. Beta", rank is 1.


class PromptResult(BaseModel):
    """The result of querying a specific AI model."""

    model_name: str  # e.g., "claude-3-5-sonnet", "gpt-4o"
    query: str
    raw_response: str
    mention: BrandMention
    latency_ms: int


class GeoSimulationSession(BaseModel):
    """A full simulation session for a specific target query across multiple models."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    website_id: uuid.UUID
    target_query: str
    target_brand_name: str

    results: list[PromptResult] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def calculate_geo_score(self) -> int:
        """Calculate a 0-100 score based on brand visibility across models."""
        if not self.results:
            return 0

        mentions = sum(1 for r in self.results if r.mention.mentioned)
        base_score = (mentions / len(self.results)) * 100

        return int(base_score)
