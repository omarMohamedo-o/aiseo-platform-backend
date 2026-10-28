"""Unit tests for Stochastic Self-Consistency & Wilson Score Confidence Intervals.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.analysis.stochastic_evaluator import StochasticEvaluator


def test_wilson_score_interval_bounds() -> None:
    # 8 mentions out of 10 runs
    ci = StochasticEvaluator.compute_wilson_score_interval(successes=8, total_trials=10)

    assert ci.point_estimate == 0.80
    assert 0.0 <= ci.lower_bound <= ci.point_estimate
    assert ci.point_estimate <= ci.upper_bound <= 1.0
    assert ci.lower_bound > 0.45  # 95% CI lower bound for 8/10 is approx 0.49
    assert ci.upper_bound < 0.98


def test_wilson_score_zero_successes() -> None:
    # 0 mentions out of 10 runs
    ci = StochasticEvaluator.compute_wilson_score_interval(successes=0, total_trials=10)

    assert ci.point_estimate == 0.0
    assert ci.lower_bound == 0.0
    assert ci.upper_bound > 0.0  # Rule of three / Wilson allows small upper probability
    assert ci.upper_bound < 0.35


def test_aggregate_runs_with_provenance_metadata() -> None:
    mentions = [True, True, True, False, True]
    sentiments = ["positive", "positive", "neutral", "neutral", "positive"]
    prompt = "What are the best industrial electrochlorination systems?"

    result = StochasticEvaluator.aggregate_runs(
        mentions=mentions,
        sentiments=sentiments,
        prompt=prompt,
        model_identifier="gpt-4o-2024-08-06",
        provider="openai",
        temperature=0.7,
    )

    assert result.total_runs == 5
    assert result.mention_count == 4
    assert result.majority_sentiment == "positive"
    assert result.sentiment_distribution["positive"] == 3
    assert result.sentiment_distribution["neutral"] == 2

    # Verify audit provenance
    meta = result.model_metadata
    assert meta.model_identifier == "gpt-4o-2024-08-06"
    assert meta.provider == "openai"
    assert meta.temperature == 0.7
    assert len(meta.prompt_hash) == 16

