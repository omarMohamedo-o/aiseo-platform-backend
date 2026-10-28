"""Unit tests for Centralized Test Configuration and Shared Fixtures.

Verifies that the test configuration accurately specifies test subjects,
corpora, topologies, and templates without hardcoded drift.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from tests.test_config import (
    PlatformTestConfig,
    TARGET_BASE_URL,
    TARGET_BRAND,
    TARGET_DOMAIN,
    TARGET_EMAIL,
    TARGET_PAGES,
    TARGET_PHONE,
    TEST_BROKEN_HTML,
    TEST_CONFIG,
    TEST_CO_CITATION_BASKETS,
    TEST_EVIDENCE_CHUNKS,
    TEST_GROUNDED_SOURCES,
    TEST_LINK_GRAPH,
    TEST_PMI_BASKETS,
    TEST_THIN_HTML,
    TEST_VALID_AEO_HTML,
    TEST_VALID_SEO_HTML,
)


def test_target_brand_config() -> None:
    assert TARGET_BRAND == "ChloroMaster"
    assert TARGET_DOMAIN == "chloromaster.com"
    assert TARGET_BASE_URL == "https://chloromaster.com"
    assert TARGET_EMAIL == "support@chloromaster.com"
    assert TARGET_PHONE == "+201012345678"
    assert len(TARGET_PAGES) >= 4
    assert TARGET_PAGES["home"] == "https://chloromaster.com"


def test_test_corpus_config() -> None:
    assert len(TEST_CO_CITATION_BASKETS) >= 4
    assert len(TEST_PMI_BASKETS) >= 4
    assert len(TEST_EVIDENCE_CHUNKS) >= 2
    assert len(TEST_GROUNDED_SOURCES) >= 2
    assert any(TARGET_BRAND.lower() in basket for basket in TEST_CO_CITATION_BASKETS)
    assert any(TARGET_BRAND in chunk for chunk in TEST_EVIDENCE_CHUNKS)


def test_test_html_templates() -> None:
    assert "<!DOCTYPE html>" in TEST_VALID_SEO_HTML
    assert TARGET_BRAND in TEST_VALID_SEO_HTML
    assert TARGET_DOMAIN in TEST_VALID_SEO_HTML

    assert "@context" in TEST_VALID_AEO_HTML
    assert TARGET_BRAND in TEST_VALID_AEO_HTML

    assert len(TEST_THIN_HTML) < 100
    assert "Missing title" in TEST_BROKEN_HTML


def test_test_topology_config() -> None:
    assert TARGET_BASE_URL in TEST_LINK_GRAPH
    assert len(TEST_LINK_GRAPH[TARGET_BASE_URL]) >= 2


def test_pytest_fixtures(
    platform_test_config: PlatformTestConfig,
    target_brand: str,
    target_domain: str,
    target_base_url: str,
    sample_valid_seo_html: str,
    sample_valid_aeo_html: str,
    sample_evidence_chunks: list[str],
    sample_internal_link_graph: dict[str, list[str]],
) -> None:
    assert target_brand == TARGET_BRAND
    assert target_domain == TARGET_DOMAIN
    assert target_base_url == TARGET_BASE_URL
    assert sample_valid_seo_html == TEST_VALID_SEO_HTML
    assert sample_valid_aeo_html == TEST_VALID_AEO_HTML
    assert sample_evidence_chunks == TEST_EVIDENCE_CHUNKS
    assert sample_internal_link_graph == TEST_LINK_GRAPH
    assert platform_test_config == TEST_CONFIG

