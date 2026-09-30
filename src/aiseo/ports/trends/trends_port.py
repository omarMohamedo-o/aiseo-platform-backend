"""Search trends capability port."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field


class TrendPoint(BaseModel):
    """Historical data point for search terms."""

    model_config = ConfigDict(frozen=True)

    date: str
    values: dict[str, float] = Field(default_factory=dict)


class TrendSeriesResult(BaseModel):
    """Normalized search trends time-series result."""

    model_config = ConfigDict(frozen=True)

    configured: bool
    provider: str
    fetched_at: str
    terms: list[str]
    points: list[TrendPoint] = Field(default_factory=list)
    message: str | None = None


@runtime_checkable
class TrendsPort(Protocol):
    """Protocol for fetching search trend velocity and seasonality."""

    async def fetch_trends(
        self,
        terms: list[str],
        geo: str = "WORLDWIDE",
        start_date: str = "12 months ago",
        category: str = "all",
    ) -> TrendSeriesResult:
        """Retrieve normalized trend time-series data for the given search terms."""
        ...
