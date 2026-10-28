"""Unit tests for AEO Information Gain & Knowledge Triple Extraction Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.aeo.information_gain import InformationGainScorer
from tests.test_config import TARGET_BRAND


def test_extract_knowledge_triples() -> None:
    text = (
        "ChloroMaster manufactures on-site sodium hypochlorite generators for industrial plants. "
        "ChloroMaster holds ISO 9001 certification for quality engineering. "
        "The system eliminates hazardous bulk chlorine gas deliveries."
    )
    triples = InformationGainScorer.extract_knowledge_triples(text, subject_entity=TARGET_BRAND)

    assert len(triples) >= 2
    preds = [t.predicate for t in triples]
    assert "produces" in preds
    assert "certified_by" in preds

    for t in triples:
        assert t.subject == TARGET_BRAND
        assert t.confidence >= 0.80
        assert len(t.object_val) > 0


def test_compute_information_gain_high_novelty() -> None:
    # Competitor corpus has generic commodity text
    competitor_corpus = [
        "We provide standard water chlorination pumps and chemical treatment services.",
        "Water disinfection equipment for municipal tanks and swimming pools.",
    ]
    # Client text has proprietary engineering specs, unique numbers, and certifications
    client_text = (
        f"{TARGET_BRAND} manufactures bipolar titanium electrolyzers producing 0.8% sodium hypochlorite. "
        f"Operating at 4.2kWh per kilogram of chlorine, {TARGET_BRAND} holds CE certifications and ISO 9001 compliance."
    )

    report = InformationGainScorer.compute_information_gain(
        target_text=client_text,
        competitor_corpus=competitor_corpus,
        brand_name=TARGET_BRAND,
    )

    assert report.novelty_score >= 50.0
    assert report.verdict in ("High Information Gain", "Moderate Novelty")
    assert len(report.unique_numerical_claims) > 0
    assert any("0.8%" in num or "4.2" in num for num in report.unique_numerical_claims)
    assert len(report.knowledge_triples) > 0


def test_compute_information_gain_redundant_content() -> None:
    # Target text is identical to competitor text
    comp = ["water chlorination systems for industrial plants"]
    target = "water chlorination systems for industrial plants"

    report = InformationGainScorer.compute_information_gain(
        target_text=target,
        competitor_corpus=comp,
        brand_name="BrandX",
    )

    assert report.novelty_score == 0.0
    assert report.verdict == "Redundant Commodity"
    assert report.overlap_ratio == 1.0

