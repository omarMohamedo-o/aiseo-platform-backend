"""Enterprise Generative Engine Optimization (GEO) Audit Engine.

Consolidates multi-model AI visibility, atomic claim faithfulness, AEO snippet
potential, and GLLM citation attribution into an authoritative unified GEO Index.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from aiseo.application.analysis.stochastic_evaluator import ConfidenceInterval, StochasticEvaluator
from aiseo.application.evaluation.claim_verifier import ClaimVerifier
from aiseo.application.ml.aeo_predictor import AeoFeatureVector, AeoRankPredictor


@dataclass(frozen=True)
class GeoAuditReport:
    """Unified enterprise assessment of generative AI search engine visibility."""
    brand_name: str
    domain: str
    overall_geo_index: float  # Scale 0 - 100
    market_tier: str  # Market Leader / Challenger / Emerging / At Risk
    mention_rate_ci: ConfidenceInterval
    factual_truth_score: float  # 0 - 100
    aeo_snippet_score: float  # 0 - 100
    citation_attribution_score: float  # 0 - 100
    supported_claims_count: int
    contradicted_claims_count: int
    unsupported_claims_count: int
    strategic_summary: str
    actionable_remediations: list[str]


class GeoAuditEngine:
    """Unified evaluator for Generative Engine Optimization (GEO)."""

    @classmethod
    def evaluate(
        cls,
        brand_name: str,
        domain: str,
        model_mentions: Sequence[bool],
        ai_responses: Sequence[str],
        crawled_evidence_chunks: Sequence[str],
        page_html: str,
        citation_count: int = 1,
    ) -> GeoAuditReport:
        """Computes comprehensive GEO visibility, factual truth, and AEO metrics."""
        n_runs = len(model_mentions)
        if n_runs == 0:
            raise ValueError("Must provide at least one model mention record.")

        # 1. Mention Rate & Wilson 95% Confidence Interval
        successes = sum(1 for m in model_mentions if m)
        ci = StochasticEvaluator.compute_wilson_score_interval(successes, n_runs)
        visibility_pct = ci.point_estimate * 100.0

        # 2. Claim-Level Factual Verification across AI responses
        combined_text = " ".join(ai_responses)
        claim_summary = ClaimVerifier.verify_answer(
            generated_answer=combined_text,
            brand_name=brand_name,
            evidence_chunks=crawled_evidence_chunks,
        )

        truth_score = claim_summary.empirical_truth_score

        # 3. AEO Snippet Potential
        aeo_features = AeoRankPredictor.extract_features(page_html)
        aeo_res = AeoRankPredictor.predict(aeo_features)
        aeo_score = aeo_res.predicted_aeo_score

        # 4. GLLM Citation Attribution Score
        citation_score = min(100.0, float(citation_count * 35.0))

        # 5. Consolidated GEO Visibility Index
        # Weights: 35% AI Visibility, 25% Factual Truth, 20% AEO Snippet, 20% Citation Attribution
        geo_index = (
            (0.35 * visibility_pct)
            + (0.25 * truth_score)
            + (0.20 * aeo_score)
            + (0.20 * citation_score)
        )
        geo_index = round(min(100.0, max(0.0, geo_index)), 1)

        # Market Tier
        if geo_index >= 80.0:
            tier = "Market Leader"
            summary = f"{brand_name} holds dominant authoritative visibility across generative AI engines with strong factual grounding."
        elif geo_index >= 60.0:
            tier = "Challenger"
            summary = f"{brand_name} shows competitive generative visibility but has upside in citation density and snippet extraction."
        elif geo_index >= 40.0:
            tier = "Emerging"
            summary = f"{brand_name} is referenced inconsistently by AI engines, requiring structured data and AEO direct answer optimization."
        else:
            tier = "At Risk"
            summary = f"{brand_name} suffers from severe generative omission or factual hallucinations in AI answer models."

        # Actionable recommendations
        remediations: list[str] = []
        if claim_summary.contradicted_claims > 0:
            remediations.append("High Priority: Resolve factual contradictions identified in AI answers by publishing clear canonical specification tables.")
        if aeo_score < 70.0:
            remediations.extend(aeo_res.optimization_recommendations[:2])
        if visibility_pct < 60.0:
            remediations.append("Expand multi-lens buyer FAQ content and third-party citation PR to increase AI model presence.")

        return GeoAuditReport(
            brand_name=brand_name,
            domain=domain,
            overall_geo_index=geo_index,
            market_tier=tier,
            mention_rate_ci=ci,
            factual_truth_score=truth_score,
            aeo_snippet_score=aeo_score,
            citation_attribution_score=citation_score,
            supported_claims_count=claim_summary.supported_claims,
            contradicted_claims_count=claim_summary.contradicted_claims,
            unsupported_claims_count=claim_summary.unsupported_claims,
            strategic_summary=summary,
            actionable_remediations=remediations,
        )

