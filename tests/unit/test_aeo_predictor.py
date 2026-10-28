"""Unit tests for Machine Learning AEO Rank Predictor.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.ml.aeo_predictor import AeoFeatureVector, AeoRankPredictor
from tests.test_config import (
    TEST_BROKEN_HTML,
    TEST_THIN_HTML,
    TEST_VALID_AEO_HTML,
)


def test_predict_high_tier_content() -> None:
    html = TEST_VALID_AEO_HTML
    features = AeoRankPredictor.extract_features(html)
    assert features.has_schema_org is True
    assert features.has_faq_section is True
    assert features.bullet_list_count >= 3
    assert features.table_count >= 1

    prediction = AeoRankPredictor.predict(features)
    assert prediction.predicted_aeo_score >= 70.0
    assert prediction.inclusion_tier in ("High", "Moderate")
    assert len(prediction.top_positive_factors) >= 3


def test_predict_thin_content_generates_recommendations() -> None:
    thin_html = TEST_THIN_HTML
    features = AeoRankPredictor.extract_features(thin_html)
    prediction = AeoRankPredictor.predict(features)

    assert prediction.predicted_aeo_score < 40.0
    assert prediction.inclusion_tier == "Low"
    assert len(prediction.optimization_recommendations) >= 3
    assert any("Schema.org" in r for r in prediction.optimization_recommendations)

