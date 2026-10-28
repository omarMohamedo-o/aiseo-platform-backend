"""Pytest configuration and global shared fixtures for AISEO platform tests.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from tests.test_config import (
    PlatformTestConfig,
    TEST_CONFIG,
    TARGET_BRAND,
    TARGET_DOMAIN,
    TARGET_BASE_URL,
    TEST_VALID_SEO_HTML,
    TEST_VALID_AEO_HTML,
    TEST_THIN_HTML,
    TEST_BROKEN_HTML,
    TEST_CO_CITATION_BASKETS,
    TEST_PMI_BASKETS,
    TEST_EVIDENCE_CHUNKS,
    TEST_GROUNDED_SOURCES,
    TEST_LINK_GRAPH,
)


@pytest.fixture(scope="session")
def platform_test_config() -> PlatformTestConfig:
    """Provides access to the master test configuration."""
    return TEST_CONFIG


@pytest.fixture
def target_brand() -> str:
    """Primary test brand name."""
    return TARGET_BRAND


@pytest.fixture
def target_domain() -> str:
    """Primary test domain."""
    return TARGET_DOMAIN


@pytest.fixture
def target_base_url() -> str:
    """Primary test base URL."""
    return TARGET_BASE_URL


@pytest.fixture
def sample_valid_seo_html() -> str:
    """Valid HTML template containing full technical SEO signals."""
    return TEST_VALID_SEO_HTML


@pytest.fixture
def sample_valid_aeo_html() -> str:
    """Valid HTML template optimized for Answer Engine Optimization (AEO)."""
    return TEST_VALID_AEO_HTML


@pytest.fixture
def sample_thin_html() -> str:
    """Thin HTML content snippet."""
    return TEST_THIN_HTML


@pytest.fixture
def sample_broken_html() -> str:
    """Broken HTML content missing critical tags."""
    return TEST_BROKEN_HTML


@pytest.fixture
def sample_co_citation_baskets() -> list[list[str]]:
    """Co-citation baskets for data mining."""
    return TEST_CO_CITATION_BASKETS


@pytest.fixture
def sample_pmi_baskets() -> list[list[str]]:
    """PMI co-occurrence baskets for collocations."""
    return TEST_PMI_BASKETS


@pytest.fixture
def sample_evidence_chunks() -> list[str]:
    """Authentic crawled evidence chunks for factual grounding."""
    return TEST_EVIDENCE_CHUNKS


@pytest.fixture
def sample_grounded_sources() -> list[tuple[str, str]]:
    """URL and content chunk pairs for GLLM citation testing."""
    return TEST_GROUNDED_SOURCES


@pytest.fixture
def sample_internal_link_graph() -> dict[str, list[str]]:
    """Domain link topology graph for PageRank testing."""
    return TEST_LINK_GRAPH

