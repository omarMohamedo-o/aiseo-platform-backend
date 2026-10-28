"""Unit tests for Enterprise Grounded LLM (GLLM) Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.gllm.gllm_engine import GllmEngine
from tests.test_config import (
    TARGET_BRAND,
    TEST_CONFIG,
    TEST_GROUNDED_SOURCES,
)


def test_gllm_engine_grounded_execution() -> None:
    engine = GllmEngine(dp_threshold=0.60)
    prompt = TEST_CONFIG.corpus.primary_buyer_query
    sources = TEST_GROUNDED_SOURCES

    report = engine.execute_grounded_pipeline(
        prompt=prompt,
        retrieved_sources=sources,
        target_brand=TARGET_BRAND,
    )

    assert report.original_prompt == prompt
    assert report.target_brand == TARGET_BRAND
    assert len(report.decomposed_queries) >= 3
    assert len(report.citations) == 2
    assert "[1]" in report.synthesized_grounded_answer
    assert "[2]" in report.synthesized_grounded_answer
    assert report.is_mathematically_grounded is True
    assert report.verdict == "Grounded Search Result"

