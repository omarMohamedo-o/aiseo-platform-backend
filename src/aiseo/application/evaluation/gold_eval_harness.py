"""Gold Benchmark Evaluation Harness and Multi-Judge Agreement Engine.

Computes Precision, Recall, F1, Accuracy, and Cohen's Kappa Inter-Judge Agreement
to provide verifiable empirical accuracy metrics for enterprise clients.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from aiseo.infrastructure.evaluation.gold_dataset import GOLD_EVALUATION_DATASET, GoldExample


@dataclass(frozen=True)
class ClassificationMetrics:
    """Binary or multiclass evaluation metrics."""
    sample_size: int
    precision: float
    recall: float
    f1_score: float
    accuracy: float


@dataclass(frozen=True)
class InterJudgeAgreement:
    """Statistical measurement of agreement between independent judge models."""
    sample_size: int
    observed_agreement: float
    expected_chance_agreement: float
    cohens_kappa: float
    interpretation: str  # Near Perfect, Substantial, Moderate, Fair, Poor


class GoldEvaluationHarness:
    """Evaluation framework for benchmark validation and judge calibration."""

    @classmethod
    def evaluate_binary(cls, y_true: Sequence[bool], y_pred: Sequence[bool]) -> ClassificationMetrics:
        """Calculates Precision, Recall, F1, and Accuracy on binary predictions."""
        n = len(y_true)
        if n == 0 or n != len(y_pred):
            return ClassificationMetrics(sample_size=0, precision=0.0, recall=0.0, f1_score=0.0, accuracy=0.0)

        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt and yp)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if not yt and yp)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt and not yp)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if not yt and not yp)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (tp + tn) / n

        return ClassificationMetrics(
            sample_size=n,
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            accuracy=round(accuracy, 4),
        )

    @classmethod
    def compute_cohens_kappa(
        cls,
        ratings_a: Sequence[str],
        ratings_b: Sequence[str],
    ) -> InterJudgeAgreement:
        """Computes Cohen's Kappa measuring agreement between two independent judges."""
        n = len(ratings_a)
        if n == 0 or n != len(ratings_b):
            return InterJudgeAgreement(0, 0.0, 0.0, 0.0, "Invalid Data")

        # 1. Observed agreement P_o
        agreements = sum(1 for a, b in zip(ratings_a, ratings_b) if a == b)
        p_o = agreements / n

        # 2. Expected chance agreement P_e
        counts_a = Counter(ratings_a)
        counts_b = Counter(ratings_b)
        all_categories = set(counts_a.keys()) | set(counts_b.keys())

        p_e = sum(
            (counts_a[cat] / n) * (counts_b[cat] / n)
            for cat in all_categories
        )

        # 3. Kappa = (P_o - P_e) / (1 - P_e)
        if abs(1.0 - p_e) < 1e-9:
            kappa = 1.0  # Perfect agreement on unanimous category
        else:
            kappa = (p_o - p_e) / (1.0 - p_e)

        kappa = round(max(-1.0, min(1.0, kappa)), 4)

        # Landis & Koch (1977) interpretation
        if kappa > 0.80:
            interpretation = "Near Perfect Agreement"
        elif kappa > 0.60:
            interpretation = "Substantial Agreement"
        elif kappa > 0.40:
            interpretation = "Moderate Agreement"
        elif kappa > 0.20:
            interpretation = "Fair Agreement"
        elif kappa >= 0.0:
            interpretation = "Slight Agreement"
        else:
            interpretation = "Poor Agreement (Worse than Chance)"

        return InterJudgeAgreement(
            sample_size=n,
            observed_agreement=round(p_o, 4),
            expected_chance_agreement=round(p_e, 4),
            cohens_kappa=kappa,
            interpretation=interpretation,
        )

