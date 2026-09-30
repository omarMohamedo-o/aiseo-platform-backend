"""Application service for running prompts concurrently across multiple AI engines."""
from __future__ import annotations

import asyncio
import time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from aiseo.infrastructure.configuration.registry import Registry
from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest


class ProviderExecutionResult(BaseModel):
    """The result of querying an AI provider with a specific question."""

    model_config = ConfigDict(frozen=True)

    provider: str
    question: str
    status: str  # "completed" | "failed"
    answer: str = ""
    citations: list[str] = Field(default_factory=list)
    latency_ms: int = 0
    error_message: str | None = None


class PromptExecutorService:
    """Dispatches questions to multiple configured AI providers in parallel."""

    def __init__(self, llm_registry: Registry[LlmProvider]) -> None:
        self._registry = llm_registry

    async def execute_single(
        self,
        provider_name: str,
        question: str,
        system_prompt: str | None = None,
    ) -> ProviderExecutionResult:
        start_time = time.monotonic()
        try:
            provider = self._registry.resolve(provider_name)
            req = LlmRequest(prompt=question, system=system_prompt, temperature=0.2)
            response = await provider.generate(req)
            elapsed_ms = int((time.monotonic() - start_time) * 1000)

            return ProviderExecutionResult(
                provider=provider_name,
                question=question,
                status="completed",
                answer=response.text,
                latency_ms=elapsed_ms,
            )
        except Exception as exc:
            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            return ProviderExecutionResult(
                provider=provider_name,
                question=question,
                status="failed",
                answer="",
                latency_ms=elapsed_ms,
                error_message=str(exc),
            )

    async def execute_matrix(
        self,
        providers: list[str],
        questions: list[str],
        system_prompt: str | None = None,
    ) -> list[ProviderExecutionResult]:
        """Query multiple providers with multiple questions concurrently."""
        tasks: list[Any] = []
        for provider_name in providers:
            for q in questions:
                tasks.append(
                    self.execute_single(provider_name, q, system_prompt)
                )

        results: list[ProviderExecutionResult] = await asyncio.gather(*tasks)
        return results
