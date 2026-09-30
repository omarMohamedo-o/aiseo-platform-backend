"""Configuration for Google Trends and search volume time-series."""
from __future__ import annotations

from pydantic import BaseModel, Field


class TrendsConfig(BaseModel):
    """Google Trends adapter configuration."""

    api_endpoint: str = Field(
        default="https://trends.google.com/trends/api/explore",
        description="Google Trends explore endpoint",
    )
    timeout_seconds: float = Field(default=15.0, description="Request timeout in seconds")
    default_geo: str = Field(default="US", description="Default geographic region code")
    default_timeframe: str = Field(default="today 12-m", description="Default historical timeframe")
