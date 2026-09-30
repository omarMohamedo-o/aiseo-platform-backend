"""Domain models for SERP (Search Engine Results Page) data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitorResult(BaseModel):
    """A competitor found in the same SERP for a given query."""

    model_config = ConfigDict(extra="forbid")

    domain: str
    position: int
    url: str
    snippet: str | None = None


class SerpResult(BaseModel):
    """A single SERP observation for a keyword query at a point in time.

    Tracks where the client's website ranks for a given search query,
    alongside competitor positions and search metadata.
    """

    model_config = ConfigDict(extra="forbid")

    query: str
    position: int | None = None  # None = website not found in results
    url: str | None = None  # Which page of our site ranked
    snippet: str | None = None
    serp_features: list[str] = []  # "featured_snippet", "people_also_ask", "ai_overview", ...
    competitors: list[CompetitorResult] = []
    search_volume: int | None = None
    keyword_difficulty: float | None = None
    scanned_at: datetime | None = None
