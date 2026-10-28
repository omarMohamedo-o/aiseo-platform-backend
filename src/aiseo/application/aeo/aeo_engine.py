"""Enterprise Answer Engine Optimization (AEO) Engine.

Dedicated engine for direct AI answer box extraction, information gain novelty scoring,
knowledge triple generation, and featured snippet optimization.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from aiseo.application.aeo.information_gain import InformationGainReport, InformationGainScorer, KnowledgeTriple
from aiseo.application.ml.aeo_predictor import AeoPredictionResult, AeoRankPredictor


@dataclass(frozen=True)
class AeoAuditReport:
    """Consolidated Answer Engine Optimization (AEO) assessment report."""
    brand_name: str
    predicted_aeo_score: float  # Scale 0 - 100
    inclusion_tier: str  # High / Moderate / Low
    information_gain_score: float  # Scale 0 - 100
    information_gain_verdict: str
    extracted_knowledge_triples: list[KnowledgeTriple]
    unique_numerical_claims: list[str]
    lead_answer_paragraph_present: bool
    top_positive_factors: list[str]
    optimization_recommendations: list[str]


class AeoEngine:
    """Dedicated enterprise Answer Engine Optimization (AEO) engine."""

    @classmethod
    def evaluate(
        cls,
        brand_name: str,
        page_html: str,
        competitor_corpus: Sequence[str] | None = None,
    ) -> AeoAuditReport:
        """Performs comprehensive AEO assessment combining snippet extraction and information gain."""
        # 1. Feature extraction and snippet inclusion prediction
        features = AeoRankPredictor.extract_features(page_html)
        prediction = AeoRankPredictor.predict(features)

        # 2. Information gain and knowledge triple extraction
        corpus = competitor_corpus or []
        body_text = page_html
        gain_report = InformationGainScorer.compute_information_gain(
            target_text=body_text,
            competitor_corpus=corpus,
            brand_name=brand_name,
        )

        # 3. Consolidated recommendations
        recommendations = list(prediction.optimization_recommendations)
        if gain_report.novelty_score < 40.0:
            recommendations.append("Information Gain Warning: Content is statistically similar to existing competitor text; publish proprietary data or laboratory measurements.")

        return AeoAuditReport(
            brand_name=brand_name,
            predicted_aeo_score=prediction.predicted_aeo_score,
            inclusion_tier=prediction.inclusion_tier,
            information_gain_score=gain_report.novelty_score,
            information_gain_verdict=gain_report.verdict,
            extracted_knowledge_triples=gain_report.knowledge_triples,
            unique_numerical_claims=gain_report.unique_numerical_claims,
            lead_answer_paragraph_present=features.has_direct_answer_paragraph,
            top_positive_factors=prediction.top_positive_factors,
            optimization_recommendations=recommendations,
        )

