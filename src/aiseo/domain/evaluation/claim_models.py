"""Domain models for Atomic Claim Extraction and NLI-Style Verification.

Decomposes complex generative AI answers into atomic factual claims,
evaluating them against crawled ground-truth DOM chunks.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field


class ClaimVerdict(str, enum.Enum):
    """NLI-style verification status of an atomic proposition."""
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"


class ClaimCategory(str, enum.Enum):
    """Semantic category of the extracted factual claim."""
    FEATURE_SPECIFICATION = "feature_specification"
    CERTIFICATION_COMPLIANCE = "certification_compliance"
    COMMERCIAL_PRICING = "commercial_pricing"
    COMPETITIVE_COMPARISON = "competitive_comparison"
    GENERAL_ATTRIBUTE = "general_attribute"


@dataclass(frozen=True)
class AtomicClaim:
    """Individual atomic proposition asserted by an AI engine."""
    claim_text: str
    subject_brand: str
    category: ClaimCategory
    polarity: str = "positive"  # positive / negative assertion


@dataclass(frozen=True)
class ClaimVerificationResult:
    """Evaluation result for an atomic proposition against ground-truth evidence."""
    claim: AtomicClaim
    verdict: ClaimVerdict
    confidence: float
    evidence_chunk: str
    reasoning: str


@dataclass(frozen=True)
class AnswerVerificationSummary:
    """Aggregated claim-level verification report for an AI generated response."""
    total_claims: int
    supported_claims: int
    contradicted_claims: int
    unsupported_claims: int
    support_ratio: float
    contradiction_ratio: float
    unsupported_ratio: float
    empirical_truth_score: float  # Scale 0.0 - 100.0
    verified_results: list[ClaimVerificationResult] = field(default_factory=list)
