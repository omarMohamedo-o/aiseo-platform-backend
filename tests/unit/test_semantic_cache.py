import asyncio
import time
import pytest

from aiseo.adapters.cache.tiered_semantic_cache import TieredSemanticCacheAdapter
from aiseo.application.analysis.prompt_executor import PromptExecutorService, ProviderExecutionResult
from aiseo.infrastructure.configuration.registry import Registry
from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest, LlmResponse


class MockLlmProvider:
    def __init__(self, answer: str = "Test response"):
        self.call_count = 0
        self._answer = answer

    async def generate(self, request: LlmRequest) -> LlmResponse:
        self.call_count += 1
        return LlmResponse(
            text=f"{self._answer} (call {self.call_count})",
            provider="mock-ai",
            model="mock-model",
            input_tokens=10,
            output_tokens=20,
        )


@pytest.mark.asyncio
async def test_exact_cache_get_set_and_expiry():
    cache = TieredSemanticCacheAdapter(default_ttl=1)
    await cache.set("key1", "value1", ttl_seconds=1)

    # Immediate hit
    val = await cache.get("key1")
    assert val == "value1"

    # Wait for TTL expiration
    await asyncio.sleep(1.1)
    expired_val = await cache.get("key1")
    assert expired_val is None


@pytest.mark.asyncio
async def test_semantic_cache_hit_and_miss():
    cache = TieredSemanticCacheAdapter(default_ttl=3600)
    query = "What is the enterprise pricing tier for Acme Corp?"
    await cache.set_semantic(query, {"tier": "Enterprise", "price": "$999/mo"})

    # High similarity variant
    similar_query = "What is enterprise pricing tier for Acme Corp"
    hit = await cache.get_semantic(similar_query, similarity_threshold=0.85)
    assert hit is not None
    assert hit["price"] == "$999/mo"

    # Completely different query
    different_query = "How to integrate Webhook notifications with Slack?"
    miss = await cache.get_semantic(different_query, similarity_threshold=0.85)
    assert miss is None


@pytest.mark.asyncio
async def test_prompt_executor_semantic_caching():
    cache = TieredSemanticCacheAdapter(default_ttl=3600)
    mock_llm = MockLlmProvider(answer="Acme is rated #1 in GEO visibility.")

    registry: Registry[LlmProvider] = Registry()
    registry.register("mock-ai", lambda: mock_llm)

    executor = PromptExecutorService(llm_registry=registry, cache=cache)

    q1 = "Best AI search engine optimization software for enterprise brands"
    res1 = await executor.execute_single("mock-ai", q1)
    assert res1.status == "completed"
    assert res1.cached is False
    assert mock_llm.call_count == 1
    assert "Acme is rated #1" in res1.answer

    # Second near-identical query should hit semantic cache and NOT increment call_count
    q2 = "Best AI search engine optimization software for enterprise"
    res2 = await executor.execute_single("mock-ai", q2)
    assert res2.status == "completed"
    assert res2.cached is True
    assert res2.latency_ms == 1
    assert mock_llm.call_count == 1  # LLM was shielded by the cache!
