"""Abstract port interface for Tiered Response Caching and Semantic Rate-Limit Shielding."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CachePort(ABC):
    """Port for exact-key and semantic similarity-based caching with TTL."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Retrieve exact key cached value."""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Store exact key cached value with TTL."""
        raise NotImplementedError

    @abstractmethod
    async def get_semantic(self, query: str, similarity_threshold: float = 0.95) -> Any | None:
        """Retrieve cached value if an existing query has semantic similarity >= similarity_threshold."""
        raise NotImplementedError

    @abstractmethod
    async def set_semantic(self, query: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Index query and value in semantic cache with TTL."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Invalidate key from cache."""
        raise NotImplementedError

