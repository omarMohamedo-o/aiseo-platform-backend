"""Platform Configuration domain models.

These configurations are global across the entire platform and manage
how the system behaves (e.g., AI routing rules, scoring weights).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class ScoringWeights(BaseModel):
    """The weights used to calculate the overall SEO/AEO/GEO scores."""

    model_config = ConfigDict(extra="forbid")

    technical_weight: float = Field(0.25, ge=0.0, le=1.0)
    onpage_weight: float = Field(0.35, ge=0.0, le=1.0)
    content_weight: float = Field(0.20, ge=0.0, le=1.0)
    rankings_weight: float = Field(0.20, ge=0.0, le=1.0)

    def validate_weights(self) -> None:
        """Ensure weights sum to 1.0 (100%)."""
        total = (
            self.technical_weight + self.onpage_weight + self.content_weight + self.rankings_weight
        )
        if not (0.99 <= total <= 1.01):  # Float tolerance
            raise ValueError(f"Scoring weights must sum to 1.0, got {total}")


class PlatformConfig(BaseModel):
    """Global configuration for the platform."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    version: int = 1

    # AI Routing: TaskType (str) -> Model Name (str)
    ai_routing_rules: dict[str, str] = {}

    # Global Scoring Algorithm
    scoring_weights: ScoringWeights = Field(default_factory=ScoringWeights)

    # Crawler Settings
    global_crawler_delay_ms: int = 1000

    updated_at: datetime = datetime.now(UTC)
    updated_by: uuid.UUID | None = None  # AdminUser ID

    def update_routing_rule(
        self, task: str, target_model: str, admin_id: uuid.UUID
    ) -> PlatformConfig:
        """Change which AI model handles a specific task."""
        new_rules = self.ai_routing_rules.copy()
        new_rules[task] = target_model

        return self.model_copy(
            update={
                "ai_routing_rules": new_rules,
                "version": self.version + 1,
                "updated_at": datetime.now(UTC),
                "updated_by": admin_id,
            }
        )
