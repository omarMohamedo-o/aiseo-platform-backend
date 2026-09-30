"""Model Router for the AI Gateway.

Reads routing configurations and returns the appropriate Model Provider
(Adapter) to the business logic, enabling dynamic model switching.
"""

from __future__ import annotations

from enum import Enum

from ai.gateway.interfaces.text_model import LlmProvider
from ai.gateway.registry import ModelRegistry, ModelType


class TaskType(str, Enum):
    CONTENT_GENERATION = "content_generation"
    SEO_OPTIMIZATION = "seo_optimization"
    IMAGE_ANALYSIS = "image_analysis"
    EMBEDDING_GENERATION = "embedding_generation"


class ModelRouter:
    """Routes tasks to the appropriate model provider based on configuration."""

    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry
        # In a real app, this mapping would come from a DB via Admin UI
        self._routing_rules: dict[TaskType, str] = {
            TaskType.CONTENT_GENERATION: "mock-llm-fast",
            TaskType.SEO_OPTIMIZATION: "mock-llm-smart",
        }
        self._providers: dict[str, LlmProvider] = {}

    def register_provider(self, name: str, provider: LlmProvider) -> None:
        """Register a concrete adapter instance (called during app startup)."""
        self._providers[name] = provider

    def get_text_model(self, task: TaskType) -> LlmProvider:
        """Get the configured text model for a specific task."""
        # 1. Check routing rules
        provider_name = self._routing_rules.get(task)
        if not provider_name:
            # Fallback to the first active text model if no rule exists
            active = self._registry.get_active_models(ModelType.TEXT)
            if not active:
                raise RuntimeError("No active text models available in registry.")
            provider_name = active[0].name

        # 2. Return the instantiated provider adapter
        provider = self._providers.get(provider_name)
        if not provider:
            raise RuntimeError(f"Provider adapter '{provider_name}' not registered.")

        return provider
