import pytest

from aiseo.infrastructure.configuration.registry import Registry


class _FakeAlgorithm:
    def __init__(self, name: str) -> None:
        self.name = name


def test_registry_resolves_registered_factory() -> None:
    registry: Registry[_FakeAlgorithm] = Registry()
    registry.register("hdbscan", lambda: _FakeAlgorithm("hdbscan"))
    registry.register("kmeans", lambda: _FakeAlgorithm("kmeans"))

    assert registry.resolve("hdbscan").name == "hdbscan"
    assert registry.resolve("kmeans").name == "kmeans"


def test_registry_raises_clear_error_for_unknown_key() -> None:
    registry: Registry[_FakeAlgorithm] = Registry()
    registry.register("hdbscan", lambda: _FakeAlgorithm("hdbscan"))

    with pytest.raises(KeyError, match="agglomerative"):
        registry.resolve("agglomerative")


def test_adding_new_algorithm_does_not_require_touching_existing_ones() -> None:
    """Open/closed check: registering a new key never mutates existing ones."""
    registry: Registry[_FakeAlgorithm] = Registry()
    registry.register("hdbscan", lambda: _FakeAlgorithm("hdbscan"))
    before = registry.resolve("hdbscan").name

    registry.register("agglomerative", lambda: _FakeAlgorithm("agglomerative"))

    assert registry.resolve("hdbscan").name == before
    assert registry.resolve("agglomerative").name == "agglomerative"
