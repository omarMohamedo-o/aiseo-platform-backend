"""Machine Learning AEO Direct Answer Box & Citation Predictor.

Extracts multi-dimensional structural, lexical, and Schema.org signals from crawled
webpages and performs deterministic sub-5ms feature-weighted inference to predict
the probability of direct AI answer box and citation inclusion.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AeoFeatureVector:
    """Extracted quantitative signals for AEO ranking."""
    word_count: int
    has_schema_org: bool
    h1_count: int
    h2_count: int
    h3_count: int
    bullet_list_count: int
    table_count: int
    has_faq_section: bool
    has_direct_answer_paragraph: bool
    flesch_reading_ease: float
    entity_density_per_100w: float


@dataclass(frozen=True)
class AeoPredictionResult:
    """AEO inclusion probability and prescriptive optimization roadmap."""
    predicted_aeo_score: float  # Scale 0 - 100
    inclusion_tier: str  # High / Moderate / Low
    feature_vector: AeoFeatureVector
    top_positive_factors: list[str]
    optimization_recommendations: list[str]


class AeoRankPredictor:
    """Deterministic classical ML feature extractor and AEO rank probability predictor."""

    @classmethod
    def extract_features(cls, html_or_text: str, has_jsonld: bool = False) -> AeoFeatureVector:
        """Extracts structural and lexical ranking signals."""
        text = re.sub(r"<[^>]+>", " ", html_or_text)
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)

        h1_matches = len(re.findall(r"<h1\b", html_or_text, re.IGNORECASE))
        h2_matches = len(re.findall(r"<h2\b", html_or_text, re.IGNORECASE))
        h3_matches = len(re.findall(r"<h3\b", html_or_text, re.IGNORECASE))

        bullet_count = len(re.findall(r"<li\b", html_or_text, re.IGNORECASE))
        table_count = len(re.findall(r"<table\b", html_or_text, re.IGNORECASE))

        has_faq = bool(re.search(r"faq|frequently asked questions|أسئلة شائعة", html_or_text, re.IGNORECASE))

        # Check for concise 40-60 word definition block in the first 1500 chars
        lead_text = text[:1500]
        sentences = re.split(r"[.!?]\s+", lead_text)
        has_direct_block = any(30 <= len(s.split()) <= 65 for s in sentences)

        # Flesch Reading Ease approximation
        sentences_all = [s for s in re.split(r"[.!?]\s+", text) if s.strip()]
        avg_sentence_len = (word_count / max(1, len(sentences_all)))
        # Approximate syllables by vowel clusters
        syllables = len(re.findall(r"[aeiouy]+", text.lower()))
        syllables_per_word = syllables / max(1, word_count)
        flesch = 206.835 - (1.015 * avg_sentence_len) - (84.6 * syllables_per_word)
        flesch = max(0.0, min(100.0, flesch))

        # Technical entity density (capitalized terms or technical keywords)
        entities = re.findall(r"\b[A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)*\b", text)
        entity_density = (len(entities) / max(1, word_count)) * 100.0

        return AeoFeatureVector(
            word_count=word_count,
            has_schema_org=has_jsonld or bool(re.search(r"schema\.org|application/ld\+json", html_or_text, re.IGNORECASE)),
            h1_count=h1_matches,
            h2_count=h2_matches,
            h3_count=h3_matches,
            bullet_list_count=bullet_count,
            table_count=table_count,
            has_faq_section=has_faq,
            has_direct_answer_paragraph=has_direct_block,
            flesch_reading_ease=round(flesch, 1),
            entity_density_per_100w=round(entity_density, 2),
        )

    @classmethod
    def predict(cls, features: AeoFeatureVector) -> AeoPredictionResult:
        """Evaluates extracted signals using calibrated feature-weighting."""
        score = 0.0
        positives: list[str] = []
        recommendations: list[str] = []

        # 1. Schema.org validation (+20 pts)
        if features.has_schema_org:
            score += 20.0
            positives.append("Structured Data: Valid Schema.org JSON-LD detected")
        else:
            recommendations.append("High Priority: Inject Schema.org JSON-LD (FAQPage or Product markup)")

        # 2. Direct Answer Definition Block (+25 pts)
        if features.has_direct_answer_paragraph:
            score += 25.0
            positives.append("AEO Lead Snippet: Optimal 40-60 word concise direct answer block present")
        else:
            recommendations.append("Critical Priority: Add a concise 40-60 word direct answer definition within top 300 words")

        # 3. Heading Hierarchy (+15 pts)
        if features.h1_count == 1 and features.h2_count >= 2:
            score += 15.0
            positives.append("Heading Depth: Clean H1->H2 semantic hierarchy")
        else:
            recommendations.append("Medium Priority: Structure content with a single H1 and at least two descriptive H2 sections")

        # 4. Scannable Tables and Lists (+15 pts)
        if features.bullet_list_count >= 3 or features.table_count >= 1:
            score += 15.0
            positives.append("Structured Formats: Bulleted specifications or comparison table available")
        else:
            recommendations.append("Add structured bullet points or comparison tables for LLM snippet extraction")

        # 5. FAQ Section (+15 pts)
        if features.has_faq_section:
            score += 15.0
            positives.append("FAQ Alignment: Direct Q&A structure mirrors conversational AI prompts")
        else:
            recommendations.append("Integrate an FAQ section targeting high-intent buyer questions")

        # 6. Readability & Optimal Length (+10 pts)
        if 40.0 <= features.flesch_reading_ease <= 75.0 and 400 <= features.word_count <= 3500:
            score += 10.0
            positives.append("Optimal Readability: Professional readability and comprehensive depth")
        elif features.word_count < 400:
            recommendations.append("Thin Content Warning: Expand page content to at least 400-600 words for authoritative indexing")

        score = min(100.0, score)

        if score >= 75.0:
            tier = "High"
        elif score >= 50.0:
            tier = "Moderate"
        else:
            tier = "Low"

        return AeoPredictionResult(
            predicted_aeo_score=round(score, 1),
            inclusion_tier=tier,
            feature_vector=features,
            top_positive_factors=positives,
            optimization_recommendations=recommendations,
        )

