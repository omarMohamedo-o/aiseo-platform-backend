"""Composition root: reads configuration, resolves providers/algorithms,
builds adapters, and wires application services. This is the ONLY module
allowed to instantiate concrete infrastructure classes directly."""

from __future__ import annotations

from dataclasses import dataclass

from aiseo.adapters.persistence.in_memory_website_repository import InMemoryWebsiteRepository
from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.infrastructure.configuration.registry import Registry
from aiseo.infrastructure.configuration.settings import Settings, load_settings
from aiseo.ports.clustering.clustering_algorithm import ClusteringAlgorithm
from aiseo.ports.persistence.website_repository import WebsiteRepository


@dataclass(frozen=True)
class ApplicationContainer:
    """Holds fully-wired application services for the process lifetime."""

    settings: Settings
    website_repository: WebsiteRepository
    register_website_service: RegisterWebsiteService
    clustering_registry: Registry[ClusteringAlgorithm]


def _build_clustering_registry() -> Registry[ClusteringAlgorithm]:
    registry: Registry[ClusteringAlgorithm] = Registry()
    # Real adapters (HDBSCAN, KMeans, ...) are registered here in later phases,
    # e.g. registry.register("hdbscan", lambda: HdbscanClusteringAlgorithm()).
    # Phase 1 intentionally ships no concrete clustering algorithm yet.
    return registry


def build_container(settings: Settings | None = None) -> ApplicationContainer:
    """Build the application container from configuration.

    Domain and application services never call this function or read
    settings themselves -- they only receive already-constructed
    dependencies through their constructors.
    """
    resolved_settings = settings or load_settings()

    website_repository: WebsiteRepository = InMemoryWebsiteRepository()
    register_website_service = RegisterWebsiteService(website_repository=website_repository)

    return ApplicationContainer(
        settings=resolved_settings,
        website_repository=website_repository,
        register_website_service=register_website_service,
        clustering_registry=_build_clustering_registry(),
    )
