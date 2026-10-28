"""Enterprise Grounded Large Language Model (GLLM) Engine.

Dedicated engine for search-grounded generative LLM execution, multi-hop query
fan-out decomposition, dynamic programming sequence alignment, and verifiable
footnote citation attribution.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from aiseo.application.evaluation.claim_verifier import ClaimVerifier
from aiseo.application.gllm.query_decomposer import GllmGroundedResponse, GllmQueryDecomposer, GroundedCitationAnchor
from aiseo.application.nlp.dp_aligner import DpAlignmentResult, SmithWatermanAligner


@dataclass(frozen=True)
class GllmAuditReport:
    """Consolidated GLLM search-grounding and attribution report."""
    original_prompt: str
    target_brand: str
    decomposed_queries: list[str]
    synthesized_grounded_answer: str
    citations: list[GroundedCitationAnchor]
    attribution_density: float
    dp_concordance_score: float
    is_mathematically_grounded: bool
    supported_claims_ratio: float
    verdict: str  # Grounded Search Result / Hallucinated Speculation


class GllmEngine:
    """Dedicated enterprise Grounded LLM (GLLM) search engine."""

    def __init__(self, dp_threshold: float = 0.65) -> None:
        self._aligner = SmithWatermanAligner(grounding_threshold=dp_threshold)

    def execute_grounded_pipeline(
        self,
        prompt: str,
        retrieved_sources: Sequence[tuple[str, str]],  # (url, content_chunk)
        target_brand: str,
    ) -> GllmAuditReport:
        """Executes full GLLM cycle: fan-out -> grounded synthesis -> DP alignment verification."""
        # 1. Synthesize citation-grounded response
        grounded_resp = GllmQueryDecomposer.synthesize_grounded_response(
            prompt=prompt,
            retrieved_sources=retrieved_sources,
            target_brand=target_brand,
        )

        # 2. Dynamic programming local alignment against retrieved evidence
        evidence_text = " ".join([chunk for _, chunk in retrieved_sources])
        dp_result = self._aligner.align(
            query=grounded_resp.synthesized_answer[:200],
            reference=evidence_text,
        )

        # 3. Claim verification across atomic assertions
        claim_summary = ClaimVerifier.verify_answer(
            generated_answer=grounded_resp.synthesized_answer,
            brand_name=target_brand,
            evidence_chunks=[chunk for _, chunk in retrieved_sources],
        )

        is_grounded = dp_result.is_grounded or claim_summary.support_ratio >= 0.50
        verdict = "Grounded Search Result" if is_grounded else "Hallucinated Speculation"

        return GllmAuditReport(
            original_prompt=prompt,
            target_brand=target_brand,
            decomposed_queries=grounded_resp.decomposed_queries,
            synthesized_grounded_answer=grounded_resp.synthesized_answer,
            citations=grounded_resp.citations,
            attribution_density=grounded_resp.attribution_density,
            dp_concordance_score=dp_result.concordance_ratio,
            is_mathematically_grounded=is_grounded,
            supported_claims_ratio=claim_summary.support_ratio,
            verdict=verdict,
        )

