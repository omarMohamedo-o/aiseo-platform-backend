"""Model Registry for the AI Gateway.

Stores configuration for available AI models. In a full enterprise setup (Phase C),
this data lives in PostgreSQL so the Admin can dynamically register/enable models.
For MVP, this uses an in-memory store.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ModelType(str, Enum):
    TEXT = "text"
    VISION = "vision"
    EMBEDDING = "embedding"
    RERANKER = "reranker"


class ModelStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    TESTING = "testing"


class RegisteredModel(BaseModel):
    """Configuration for an AI Model registered in the platform."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    name: str  # e.g., "claude-3-5-sonnet-20240620", "deepseek-chat"
    provider: str  # "anthropic", "gemini", "openai", "deepseek", "local"
    model_type: ModelType
    status: ModelStatus = ModelStatus.ACTIVE
    capabilities: list[str] = []
    context_window: int = 8192
    cost_per_1k_tokens: float = 0.0
    is_local: bool = False
    configuration: dict[str, str] = {}  # API keys, endpoint URLs if custom
    created_at: datetime = datetime.now(UTC)


class ModelRegistry:
    """In-memory registry of all available AI models."""

    def __init__(self) -> None:
        self._models: dict[uuid.UUID, RegisteredModel] = {}

    def register(self, model: RegisteredModel) -> None:
        """Register a new model in the platform."""
        self._models[model.id] = model

    def get_by_id(self, model_id: uuid.UUID) -> RegisteredModel | None:
        """Get a model by its unique ID."""
        return self._models.get(model_id)

    def get_active_models(self, model_type: ModelType) -> list[RegisteredModel]:
        """List all active models of a given type."""
        return [
            m
            for m in self._models.values()
            if m.model_type == model_type and m.status == ModelStatus.ACTIVE
        ]
