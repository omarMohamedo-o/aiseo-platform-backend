"""Unit tests for GLLM Query Fan-Out & Grounded Search Orchestrator.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.gllm.query_decomposer import GllmQueryDecomposer
from tests.test_config import (
    TARGET_BRAND,
    TEST_CONFIG,
    TEST_GROUNDED_SOURCES,
)


def test_query_fan_out_decomposition() -> None:
    prompt = TEST_CONFIG.corpus.primary_buyer_query
    sub_queries = GllmQueryDecomposer.decompose_query(prompt, target_brand=TARGET_BRAND)

    assert len(sub_queries) >= 3
    # Sub-queries should include brand comparison and technical specs
    assert any(TARGET_BRAND in q for q in sub_queries)
    assert any("specifications" in q.lower() or "compliance" in q.lower() for q in sub_queries)


def test_synthesize_grounded_response_with_citations() -> None:
    prompt = TEST_CONFIG.corpus.safety_buyer_query
    sources = TEST_GROUNDED_SOURCES

    response = GllmQueryDecomposer.synthesize_grounded_response(
        prompt=prompt,
        retrieved_sources=sources,
        target_brand=TARGET_BRAND,
    )

    assert len(response.citations) == 2
    assert response.citations[0].citation_id == 1
    assert response.citations[0].url == TEST_GROUNDED_SOURCES[0][0]
    assert "[1]" in response.synthesized_answer
    assert "[2]" in response.synthesized_answer
    assert response.attribution_density > 0.0

