"""Unit tests for Association Rule & Co-Citation Data Mining Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.mining.association_miner import AssociationMiner
from tests.test_config import (
    TARGET_BRAND,
    TEST_CO_CITATION_BASKETS,
    TEST_PMI_BASKETS,
)


def test_mine_co_citations_basic() -> None:
    # Co-citation baskets from centralized test config
    baskets = TEST_CO_CITATION_BASKETS

    result = AssociationMiner.mine_co_citations(baskets, min_support=0.2, min_confidence=0.5)

    assert result.total_transactions == len(baskets)
    assert TARGET_BRAND.lower() in result.frequent_items
    assert "evoqua" in result.frequent_items
    assert len(result.rules) > 0

    # Test rule fields
    first_rule = result.rules[0]
    assert first_rule.support >= 0.2
    assert first_rule.confidence >= 0.5
    assert first_rule.lift > 0.0


def test_pmi_calculation_positive_association() -> None:
    baskets = TEST_PMI_BASKETS

    result = AssociationMiner.mine_co_citations(baskets, min_support=0.2, min_confidence=0.5)
    assert len(result.pmi_scores) > 0

    # Locate the target brand pair
    target_score = next(
        (s for s in result.pmi_scores if TARGET_BRAND.lower() in (s.term_a, s.term_b)),
        None,
    )
    assert target_score is not None
    assert target_score.pmi > 0.0
    assert target_score.co_occurrence_count == 3


def test_empty_baskets_handling() -> None:
    result = AssociationMiner.mine_co_citations([])
    assert result.total_transactions == 0
    assert len(result.rules) == 0
    assert len(result.pmi_scores) == 0
