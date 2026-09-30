"""Configuration for retry backoff and circuit breaker resilience."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ResilienceConfig(BaseModel):
    """Resilience settings for external API integrations."""

    retry_max_attempts: int = Field(default=3, description="Maximum retry attempts on transient failures")
    retry_initial_delay: float = Field(default=0.5, description="Initial retry delay in seconds")
    retry_max_delay: float = Field(default=10.0, description="Maximum retry delay in seconds")
    circuit_breaker_failure_threshold: int = Field(
        default=5,
        description="Consecutive failure count to trip circuit breaker open",
    )
    circuit_breaker_recovery_timeout: float = Field(
        default=30.0,
        description="Cooldown duration before entering half-open probe state",
    )
