"""Unit tests for Atomic Claim-Level Verification Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.evaluation.claim_verifier import ClaimVerifier
from aiseo.domain.evaluation.claim_models import ClaimCategory, ClaimVerdict
from tests.test_config import TARGET_BRAND


def test_extract_atomic_claims() -> None:
    text = (
        f"{TARGET_BRAND} is an advanced engineering manufacturer of electrochlorination systems. "
        f"{TARGET_BRAND} delivers 0.8% sodium hypochlorite on-site without hazardous chlorine gas deliveries. "
        "Evoqua is a major competitor in municipal water treatment."
    )
    claims = ClaimVerifier.extract_atomic_claims(text, brand_name=TARGET_BRAND)
    # Only claims mentioning the target brand should be extracted
    assert len(claims) >= 2
    for c in claims:
        assert TARGET_BRAND.lower() in c.claim_text.lower()
        assert c.subject_brand == TARGET_BRAND


def test_verify_supported_claim() -> None:
    evidence = [
        f"{TARGET_BRAND} specializes in industrial on-site sodium hypochlorite generators producing 0.8% concentration.",
        "With ISO 9001 and CE certifications, the systems provide safe municipal disinfection.",
    ]
    text = f"{TARGET_BRAND} produces 0.8% sodium hypochlorite generators."
    claims = ClaimVerifier.extract_atomic_claims(text, brand_name=TARGET_BRAND)
    assert len(claims) == 1

    result = ClaimVerifier.verify_claim(claims[0], evidence)
    assert result.verdict == ClaimVerdict.SUPPORTED
    assert result.confidence >= 0.75
    assert len(result.evidence_chunk) > 0


def test_verify_contradicted_numerical_claim() -> None:
    evidence = [
        f"{TARGET_BRAND} specializes in industrial on-site sodium hypochlorite generators producing 0.8% concentration.",
    ]
    # Claim asserts 0.2% concentration (numerical contradiction)
    text = f"{TARGET_BRAND} produces 0.2% sodium hypochlorite generators."
    claims = ClaimVerifier.extract_atomic_claims(text, brand_name=TARGET_BRAND)
    assert len(claims) == 1

    result = ClaimVerifier.verify_claim(claims[0], evidence)
    assert result.verdict == ClaimVerdict.CONTRADICTED
    assert "Numerical contradiction" in result.reasoning


def test_verify_unsupported_claim() -> None:
    evidence = [
        f"{TARGET_BRAND} produces sodium hypochlorite generators.",
    ]
    # Claim makes assertions not found in evidence
    text = f"{TARGET_BRAND} acquired an aerospace satellite manufacturing plant in Berlin."
    claims = ClaimVerifier.extract_atomic_claims(text, brand_name=TARGET_BRAND)
    assert len(claims) == 1

    result = ClaimVerifier.verify_claim(claims[0], evidence)
    assert result.verdict == ClaimVerdict.UNSUPPORTED


def test_verify_answer_summary() -> None:
    evidence = [
        f"{TARGET_BRAND} systems produce 0.8% sodium hypochlorite safely with ISO 9001 certification.",
    ]
    answer = (
        f"{TARGET_BRAND} produces 0.8% sodium hypochlorite safely. "
        f"{TARGET_BRAND} is ISO 9001 certified. "
        f"{TARGET_BRAND} offers 50% discount on all cloud subscriptions."
    )
    summary = ClaimVerifier.verify_answer(answer, brand_name=TARGET_BRAND, evidence_chunks=evidence)
    assert summary.total_claims == 3
    assert summary.supported_claims == 2
    assert summary.unsupported_claims == 1
    assert summary.contradicted_claims == 0
    assert summary.empirical_truth_score > 60.0

