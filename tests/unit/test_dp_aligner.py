"""Unit tests for Dynamic Programming Local Sequence Aligner.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.nlp.dp_aligner import SmithWatermanAligner
from tests.test_config import TARGET_BRAND


def test_align_exact_substring() -> None:
    query = "systems eliminate hazardous bulk chlorine gas deliveries"
    reference = (
        f"{TARGET_BRAND} industrial systems eliminate hazardous bulk chlorine gas deliveries "
        "by generating sodium hypochlorite on site."
    )

    aligner = SmithWatermanAligner()
    res = aligner.align(query, reference)

    assert res.is_grounded is True
    assert res.concordance_ratio >= 0.90
    assert res.aligned_query == res.aligned_reference
    assert res.ref_start_token_idx >= 0
    assert res.ref_end_token_idx > res.ref_start_token_idx


def test_align_partial_fuzzy_match() -> None:
    query = "systems eliminate risky bulk chlorine shipments"
    reference = "Our systems eliminate hazardous bulk chlorine gas deliveries safely."

    aligner = SmithWatermanAligner(grounding_threshold=0.50)
    res = aligner.align(query, reference)

    assert res.concordance_ratio > 0.40
    assert "systems eliminate" in res.aligned_query


def test_align_unrelated_text_fails_grounding() -> None:
    query = "buy cheap international flight tickets to tokyo"
    reference = f"{TARGET_BRAND} manufactures sodium hypochlorite water treatment systems."

    aligner = SmithWatermanAligner()
    res = aligner.align(query, reference)

    assert res.is_grounded is False
    assert res.concordance_ratio < 0.20

