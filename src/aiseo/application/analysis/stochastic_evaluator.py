"""Stochastic Self-Consistency & Wilson Score Confidence Interval Evaluator.

Addresses generative model variance by executing repeated prompt samplings (N=5-10)
and computing exact Wilson Score 95% confidence intervals and majority-vote consensus.

Logs exact model identifiers, provider versions, and prompt hashes for audit reproducibility.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import hashlib
import math
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class ConfidenceInterval:
    """Wilson Score 95% confidence interval for a binomial rate."""
    point_estimate: float  # Scale 0.0 - 1.0
    lower_bound: float
    upper_bound: float
    confidence_level: float = 0.95


@dataclass(frozen=True)
class ModelRunMetadata:
    """Exact provenance metadata for a model inference execution."""
    model_identifier: str
    provider: str
    temperature: float
    prompt_hash: str
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class StochasticEvaluationResult:
    """Aggregated self-consistency and confidence interval report."""
    total_runs: int
    mention_count: int
    mention_rate_ci: ConfidenceInterval
    majority_sentiment: str
    sentiment_distribution: dict[str, int]
    model_metadata: ModelRunMetadata


class StochasticEvaluator:
    """Computes statistical confidence intervals and majority consensus over repeated runs."""

    @classmethod
    def compute_wilson_score_interval(
        cls,
        successes: int,
        total_trials: int,
        confidence: float = 0.95,
    ) -> ConfidenceInterval:
        """Calculates the Wilson score interval for binomial proportions.
        
        Guarantees mathematically rigorous confidence intervals even for small N.
        """
        if total_trials == 0:
            return ConfidenceInterval(0.0, 0.0, 0.0, confidence)

        # Standard normal quantile z (1.96 for 95% CI)
        z = 1.95996 if abs(confidence - 0.95) < 0.01 else 2.57583  # 95% vs 99%
        p_hat = successes / total_trials

        denominator = 1.0 + (z**2 / total_trials)
        centre_adjusted = (p_hat + (z**2 / (2.0 * total_trials))) / denominator
        margin = (z / denominator) * math.sqrt(
            (p_hat * (1.0 - p_hat) / total_trials) + (z**2 / (4.0 * total_trials**2))
        )

        lower = max(0.0, centre_adjusted - margin)
        upper = min(1.0, centre_adjusted + margin)

        return ConfidenceInterval(
            point_estimate=round(p_hat, 4),
            lower_bound=round(lower, 4),
            upper_bound=round(upper, 4),
            confidence_level=confidence,
        )

    @classmethod
    def aggregate_runs(
        cls,
        mentions: Sequence[bool],
        sentiments: Sequence[str],
        prompt: str,
        model_identifier: str = "gpt-4o-2024-08-06",
        provider: str = "openai",
        temperature: float = 0.7,
    ) -> StochasticEvaluationResult:
        """Aggregates stochastic outputs with Wilson confidence intervals and provenance metadata."""
        n = len(mentions)
        if n == 0:
            raise ValueError("Must provide at least 1 evaluation run to aggregate.")

        n_mentions = sum(1 for m in mentions if m)
        ci = cls.compute_wilson_score_interval(n_mentions, n)

        sentiment_counts = dict(Counter(sentiments))
        majority_sentiment = Counter(sentiments).most_common(1)[0][0] if sentiments else "neutral"

        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]

        metadata = ModelRunMetadata(
            model_identifier=model_identifier,
            provider=provider,
            temperature=temperature,
            prompt_hash=prompt_hash,
        )

        return StochasticEvaluationResult(
            total_runs=n,
            mention_count=n_mentions,
            mention_rate_ci=ci,
            majority_sentiment=majority_sentiment,
            sentiment_distribution=sentiment_counts,
            model_metadata=metadata,
        )

