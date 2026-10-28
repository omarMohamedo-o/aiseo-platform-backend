"""Unit tests for Enterprise Answer Engine Optimization (AEO) Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.aeo.aeo_engine import AeoEngine
from tests.test_config import (
    TARGET_BRAND,
    TEST_CONFIG,
    TEST_VALID_AEO_HTML,
)


def test_aeo_engine_evaluation() -> None:
    html = TEST_VALID_AEO_HTML
    competitors = TEST_CONFIG.corpus.competitor_corpus

    report = AeoEngine.evaluate(
        brand_name=TARGET_BRAND,
        page_html=html,
        competitor_corpus=competitors,
    )

    assert report.brand_name == TARGET_BRAND
    assert report.predicted_aeo_score >= 60.0
    assert report.information_gain_score >= 50.0
    assert report.inclusion_tier in ("High", "Moderate")
    assert len(report.extracted_knowledge_triples) > 0
    assert len(report.top_positive_factors) > 0

