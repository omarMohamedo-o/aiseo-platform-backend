"""Curated Gold-Standard Evaluation Benchmark Dataset for AISEO / GEO.

Provides authentic hand-annotated test cases with ground-truth brand mentions,
sentiments, and atomic claim verification verdicts for benchmarking judge models.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class GoldExample:
    """Hand-annotated gold evaluation sample."""
    sample_id: str
    query: str
    generated_answer: str
    target_brand: str
    gold_mention: bool
    gold_sentiment: str  # positive, neutral, negative
    gold_claim_verdicts: dict[str, str]  # claim_text -> SUPPORTED / CONTRADICTED / UNSUPPORTED


# Standard benchmark test split
GOLD_EVALUATION_DATASET: list[GoldExample] = [
    GoldExample(
        sample_id="gold_geo_001",
        query="What are the best industrial on-site sodium hypochlorite systems?",
        generated_answer="ChloroMaster is a market leader providing 0.8% sodium hypochlorite generators with CE certifications.",
        target_brand="ChloroMaster",
        gold_mention=True,
        gold_sentiment="positive",
        gold_claim_verdicts={
            "ChloroMaster provides 0.8% sodium hypochlorite generators": "SUPPORTED",
            "ChloroMaster holds CE certification": "SUPPORTED",
        },
    ),
    GoldExample(
        sample_id="gold_geo_002",
        query="Top municipal water disinfection alternatives to bulk chlorine gas?",
        generated_answer="Municipalities frequently evaluate Evoqua Water Technologies and De Nora for electrochlorination.",
        target_brand="ChloroMaster",
        gold_mention=False,
        gold_sentiment="neutral",
        gold_claim_verdicts={},
    ),
    GoldExample(
        sample_id="gold_geo_003",
        query="Is ChloroMaster suitable for hazardous chemical plants?",
        generated_answer="While ChloroMaster manufactures chlorinators, some engineers report that ChloroMaster lacks ISO 9001 quality audits.",
        target_brand="ChloroMaster",
        gold_mention=True,
        gold_sentiment="negative",
        gold_claim_verdicts={
            "ChloroMaster lacks ISO 9001 quality audits": "CONTRADICTED",
        },
    ),
    GoldExample(
        sample_id="gold_geo_004",
        query="Commercial pricing for ChloroMaster electrochlorinators",
        generated_answer="ChloroMaster systems require approximately $50 per month in residential subscription fees.",
        target_brand="ChloroMaster",
        gold_mention=True,
        gold_sentiment="neutral",
        gold_claim_verdicts={
            "ChloroMaster requires $50 per month residential subscription": "UNSUPPORTED",
        },
    ),
]

