"""Injectable provider/algorithm registry. Not a global mutable singleton --
owned and constructed by the composition root, one instance per process."""
from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """Maps a string key (from configuration) to a factory producing an
    implementation of `T`. Adding a new provider/algorithm means registering
    a new factory here -- no conditional chains in business logic."""

    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], T]] = {}

    def register(self, key: str, factory: Callable[[], T]) -> None:
        self._factories[key] = factory

    def resolve(self, key: str) -> T:
        try:
            factory = self._factories[key]
        except KeyError as exc:
            raise KeyError(
                f"No implementation registered for key={key!r}. "
                f"Known keys: {sorted(self._factories)}"
            ) from exc
        return factory()

    def known_keys(self) -> list[str]:
        return sorted(self._factories)
