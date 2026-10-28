"""Unit tests for Domain PageRank Graph Mining Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.mining.graph_pagerank import DomainPageRankMiner
from tests.test_config import (
    TARGET_BASE_URL,
    TEST_LINK_GRAPH,
)


def test_pagerank_basic_hub_convergence() -> None:
    # A topology from centralized test config
    graph = TEST_LINK_GRAPH

    miner = DomainPageRankMiner()
    result = miner.compute_pagerank(graph)

    assert result.total_pages == 4
    assert result.iterations_to_converge > 0
    assert sum(result.scores.values()) == pytest.approx(1.0, rel=1e-4)

    # Homepage and products should have highest authority
    top_hub = result.crawl_hubs[0][0]
    assert top_hub in (TARGET_BASE_URL, f"{TARGET_BASE_URL}/products")


def test_detects_orphan_pages_and_sinks() -> None:
    graph = {
        "https://site.com": ["https://site.com/docs"],
        "https://site.com/docs": ["https://site.com/api-sink"],
        "https://site.com/orphan": [],  # No page links to /orphan
    }

    miner = DomainPageRankMiner()
    result = miner.compute_pagerank(graph)

    assert "https://site.com/orphan" in result.orphan_pages
    assert "https://site.com/api-sink" in result.authority_sinks


def test_empty_graph() -> None:
    miner = DomainPageRankMiner()
    result = miner.compute_pagerank({})
    assert result.total_pages == 0
    assert len(result.scores) == 0

