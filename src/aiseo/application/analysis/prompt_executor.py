"""Application service for running prompts concurrently across multiple AI engines."""
from __future__ import annotations

import asyncio
import time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from aiseo.infrastructure.configuration.registry import Registry
from aiseo.ports.cache.cache_port import CachePort
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
    cached: bool = False


class PromptExecutorService:
    """Dispatches questions to multiple configured AI providers in parallel with semantic caching."""

    def __init__(
        self,
        llm_registry: Registry[LlmProvider],
        cache: CachePort | None = None,
        similarity_threshold: float = 0.88,
    ) -> None:
        self._registry = llm_registry
        self._cache = cache
        self._similarity_threshold = similarity_threshold

    async def execute_single(
        self,
        provider_name: str,
        question: str,
        system_prompt: str | None = None,
    ) -> ProviderExecutionResult:
        cache_key = f"{provider_name}:{question.strip().lower()}"
        if self._cache:
            try:
                # 1. Check exact cache (O(1))
                cached_res = await self._cache.get(cache_key)
                if not cached_res:
                    # 2. Check semantic cache
                    cached_res = await self._cache.get_semantic(
                        cache_key, similarity_threshold=self._similarity_threshold
                    )

                if cached_res and isinstance(cached_res, ProviderExecutionResult):
                    return ProviderExecutionResult(
                        provider=cached_res.provider,
                        question=question,
                        status="completed",
                        answer=cached_res.answer,
                        citations=cached_res.citations,
                        latency_ms=1,
                        cached=True,
                    )
            except Exception:
                pass

        start_time = time.monotonic()
        try:
            provider = self._registry.resolve(provider_name)
            req = LlmRequest(prompt=question, system=system_prompt, temperature=0.2)
            response = await provider.generate(req)
            elapsed_ms = int((time.monotonic() - start_time) * 1000)

            result = ProviderExecutionResult(
                provider=provider_name,
                question=question,
                status="completed",
                answer=response.text,
                latency_ms=elapsed_ms,
                cached=False,
            )
            if self._cache:
                try:
                    await self._cache.set(cache_key, result, ttl_seconds=3600)
                    await self._cache.set_semantic(cache_key, result, ttl_seconds=3600)
                except Exception:
                    pass
            return result
        except Exception as exc:
            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            return ProviderExecutionResult(
                provider=provider_name,
                question=question,
                status="failed",
                answer="",
                latency_ms=elapsed_ms,
                error_message=str(exc),
                cached=False,
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
