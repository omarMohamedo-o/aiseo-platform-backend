"""Configuration for opportunity scoring algorithms and AEO/GEO scanners."""
from __future__ import annotations

from pydantic import BaseModel, Field


class OpportunityScorerConfig(BaseModel):
    """Opportunity score formula weights and normalization bounds."""

    volume_weight: float = Field(default=0.40, description="Weight factor for search volume (40%)")
    difficulty_weight: float = Field(default=0.30, description="Weight factor for keyword difficulty (30%)")
    cpc_weight: float = Field(default=0.15, description="Weight factor for CPC commercial value (15%)")
    serp_features_weight: float = Field(default=0.15, description="Weight factor for SERP features (15%)")

    max_volume_normalization: float = Field(default=40500.0, description="Volume ceiling for 100% normalization")
    max_cpc_normalization: float = Field(default=8.0, description="CPC ceiling for 100% normalization")
    max_serp_normalization: float = Field(default=8.0, description="SERP feature count ceiling for 100% normalization")


class ScoringConfig(BaseModel):
    """Engine versions for SEO, AEO, and GEO."""

    seo_version: str = Field(default="seo-v1", description="SEO model version")
    aeo_version: str = Field(default="aeo-v1", description="AEO model version")
    geo_version: str = Field(default="geo-v1", description="GEO model version")
    opportunity: OpportunityScorerConfig = Field(default_factory=OpportunityScorerConfig)
    engine_citation_shares: dict[str, float] = Field(
        default_factory=lambda: {
            "ChatGPT (Search & Browse)": 38.4,
            "Perplexity AI": 31.2,
            "Claude (Anthropic)": 17.6,
            "Google Gemini": 12.8,
        },
        description="Market share percentages for neural citation engines"
    )
