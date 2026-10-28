"""Unit tests for Gold Benchmark Evaluation Harness & Multi-Judge Agreement.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.evaluation.gold_eval_harness import GoldEvaluationHarness
from aiseo.infrastructure.evaluation.gold_dataset import GOLD_EVALUATION_DATASET


def test_evaluate_binary_metrics() -> None:
    y_true = [True, True, False, True, False, False, True]
    y_pred = [True, True, False, False, False, True, True]

    metrics = GoldEvaluationHarness.evaluate_binary(y_true, y_pred)
    assert metrics.sample_size == 7
    assert 0.0 <= metrics.precision <= 1.0
    assert 0.0 <= metrics.recall <= 1.0
    assert 0.0 <= metrics.f1_score <= 1.0
    assert metrics.accuracy > 0.50


def test_perfect_judge_agreement_kappa() -> None:
    judge_1 = ["positive", "neutral", "negative", "positive", "neutral"]
    judge_2 = ["positive", "neutral", "negative", "positive", "neutral"]

    res = GoldEvaluationHarness.compute_cohens_kappa(judge_1, judge_2)
    assert res.observed_agreement == 1.0
    assert res.cohens_kappa == 1.0
    assert res.interpretation == "Near Perfect Agreement"


def test_substantial_judge_agreement() -> None:
    judge_1 = ["positive", "neutral", "negative", "positive", "neutral", "positive", "negative"]
    judge_2 = ["positive", "neutral", "neutral", "positive", "neutral", "positive", "negative"]

    res = GoldEvaluationHarness.compute_cohens_kappa(judge_1, judge_2)
    assert res.observed_agreement > 0.80
    assert res.cohens_kappa > 0.60
    assert "Agreement" in res.interpretation


def test_gold_dataset_integrity() -> None:
    assert len(GOLD_EVALUATION_DATASET) >= 4
    for ex in GOLD_EVALUATION_DATASET:
        assert ex.sample_id.startswith("gold_geo_")
        assert len(ex.query) > 5
        assert len(ex.target_brand) > 0
        assert ex.gold_sentiment in ("positive", "neutral", "negative")

