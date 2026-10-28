"""AEO Information Gain and Knowledge Triple Extraction Engine.

Evaluates content novelty delta (Information Gain) against competitor corpora
and extracts structured (Subject, Predicate, Object) RDF Knowledge Triples
to maximize Answer Engine direct snippet extraction.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class KnowledgeTriple:
    """Structured (Subject, Predicate, Object) RDF entity relation."""
    subject: str
    predicate: str
    object_val: str
    confidence: float


@dataclass(frozen=True)
class InformationGainReport:
    """Measurement of content novelty delta against existing competitor pages."""
    novelty_score: float  # Scale 0.0 - 100.0
    unique_entities: list[str]
    unique_numerical_claims: list[str]
    overlap_ratio: float
    knowledge_triples: list[KnowledgeTriple]
    verdict: str  # High Information Gain / Redundant Commodity


class InformationGainScorer:
    """Computes information gain novelty delta and extracts knowledge triples."""

    _PREDICATE_PATTERNS = [
        (re.compile(r"\b(manufacture|manufactures|produce|produces|deliver|delivers|generate|generates|provide|provides|create|creates)\b", re.IGNORECASE), "produces"),
        (re.compile(r"\b(hold|holds|feature|features|certified with|complies with|achieve|achieved)\b", re.IGNORECASE), "certified_by"),
        (re.compile(r"\b(eliminate|eliminates|replace|replaces|prevent|prevents|avoid|avoids)\b", re.IGNORECASE), "eliminates"),
        (re.compile(r"\b(operates at|produces concentration of|yield|yields|deliver|delivers)\b", re.IGNORECASE), "operates_at"),
        (re.compile(r"\b(cost|costs|priced at|requires subscription of)\b", re.IGNORECASE), "has_cost"),
    ]

    @classmethod
    def extract_knowledge_triples(cls, text: str, subject_entity: str) -> list[KnowledgeTriple]:
        """Extracts (Subject, Predicate, Object) relational triples from text."""
        if not text or not subject_entity:
            return []

        # Strip HTML tags if present to ensure clean sentence extraction
        clean_text = re.sub(r"<[^>]+>", " ", text)
        triples: list[KnowledgeTriple] = []
        sentences = re.split(r"[.!?]\s+", clean_text)

        for sent in sentences:
            sent_clean = sent.strip()
            if not sent_clean or subject_entity.lower() not in sent_clean.lower():
                continue

            for pattern, canonical_predicate in cls._PREDICATE_PATTERNS:
                match = pattern.search(sent_clean)
                if match:
                    pred_start = match.start()
                    pred_end = match.end()

                    # Object is the clause immediately following the predicate
                    obj_clause = sent_clean[pred_end:].strip()
                    # Clean object clause up to punctuation or conjunction
                    obj_clean = re.split(r"[,;]|\band\s+", obj_clause)[0].strip()

                    if 2 <= len(obj_clean.split()) <= 16:
                        triples.append(
                            KnowledgeTriple(
                                subject=subject_entity,
                                predicate=canonical_predicate,
                                object_val=obj_clean,
                                confidence=0.88,
                            )
                        )
                    break

        return triples

    @classmethod
    def compute_information_gain(
        cls,
        target_text: str,
        competitor_corpus: Sequence[str],
        brand_name: str,
    ) -> InformationGainReport:
        """Calculates the unique informational delta of target text vs competitor corpus."""
        target_tokens = set(re.findall(r"\b[a-z0-9_-]{3,}\b", target_text.lower()))
        
        # Aggregate competitor tokens
        comp_tokens: set[str] = set()
        for comp in competitor_corpus:
            comp_tokens.update(re.findall(r"\b[a-z0-9_-]{3,}\b", comp.lower()))

        if not target_tokens:
            return InformationGainReport(0.0, [], [], 1.0, [], "Redundant Commodity")

        # 1. Unique lexical & entity delta
        unique_tokens = target_tokens - comp_tokens

        # 2. Extract unique numerical and technical specifications
        num_pattern = re.compile(r"\b\d+(?:\.\d+)?(?:%|kwh|kw|ppm|bar|m3|kg)?", re.IGNORECASE)
        target_nums = {n for n in num_pattern.findall(target_text) if any(c.isdigit() for c in n)}
        comp_nums: set[str] = set()
        for comp in competitor_corpus:
            comp_nums.update({n for n in num_pattern.findall(comp) if any(c.isdigit() for c in n)})
        unique_nums = sorted(list(target_nums - comp_nums))

        # Filter high-salience unique entities (capitalized or specific terms)
        raw_entities = set(re.findall(r"\b[A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)*\b", target_text))
        comp_entities = set()
        for comp in competitor_corpus:
            comp_entities.update(re.findall(r"\b[A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)*\b", comp))
        unique_entities = sorted(list(raw_entities - comp_entities))

        # 3. Novelty ratio calculation
        novelty_ratio = len(unique_tokens) / len(target_tokens)
        novelty_score = round(min(100.0, (novelty_ratio * 120.0) + (len(unique_nums) * 5.0)), 1)
        overlap_ratio = round(1.0 - novelty_ratio, 4)

        # 4. Extract knowledge triples
        triples = cls.extract_knowledge_triples(target_text, brand_name)

        verdict = "High Information Gain" if novelty_score >= 60.0 else "Moderate Novelty" if novelty_score >= 35.0 else "Redundant Commodity"

        return InformationGainReport(
            novelty_score=novelty_score,
            unique_entities=unique_entities,
            unique_numerical_claims=unique_nums,
            overlap_ratio=overlap_ratio,
            knowledge_triples=triples,
            verdict=verdict,
        )
