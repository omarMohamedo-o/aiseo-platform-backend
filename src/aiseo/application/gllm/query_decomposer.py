"""GLLM Multi-Hop Query Fan-Out and Grounded Search Orchestration Engine.

Emulates modern Generative Search Engines (Google AI Overviews, Perplexity Sonar,
ChatGPT Search) by decomposing high-level buyer queries into multi-hop sub-queries
and synthesizing answers with authentic inline citation anchors.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class GroundedCitationAnchor:
    """Inline numerical citation anchor linking an asserted claim to a source URL."""
    citation_id: int
    url: str
    snippet_preview: str


@dataclass(frozen=True)
class GllmGroundedResponse:
    """Complete GLLM generated response with decomposed sub-queries and citation map."""
    original_prompt: str
    decomposed_queries: list[str]
    synthesized_answer: str
    citations: list[GroundedCitationAnchor]
    attribution_density: float  # Citations per 100 words


class GllmQueryDecomposer:
    """Decomposes generative search prompts into multi-hop retrieval sub-queries."""

    @classmethod
    def decompose_query(cls, prompt: str, target_brand: str | None = None) -> list[str]:
        """Decomposes a complex prompt into 3-4 parallel atomic search queries."""
        if not prompt or len(prompt.strip()) < 5:
            return []

        clean_p = prompt.strip().rstrip("?.!")
        sub_queries: list[str] = []

        # 1. Core Technical / Commercial Intent
        sub_queries.append(clean_p)

        # 2. Extract key nouns and topics for specification query
        words = re.findall(r"\b[a-zA-Z\u0621-\u064A]{4,}\b", clean_p)
        key_topics = [w for w in words if w.lower() not in {"what", "which", "best", "where", "when", "does", "have", "more", "then", "their"}]
        topic_str = " ".join(key_topics[:3])

        if topic_str:
            sub_queries.append(f"{topic_str} technical specifications efficiency")

        # 3. Comparative query
        if target_brand:
            sub_queries.append(f"{target_brand} vs top competitors {topic_str}")
        else:
            sub_queries.append(f"top commercial alternatives {topic_str}")

        # 4. Compliance & Safety query
        if any(w in clean_p.lower() for w in ["system", "water", "chemical", "plant", "generator", "equipment"]):
            sub_queries.append(f"{topic_str} regulatory compliance safety standards")

        # Deduplicate while preserving order
        seen = set()
        unique_queries = []
        for q in sub_queries:
            q_norm = q.lower()
            if q_norm not in seen:
                seen.add(q_norm)
                unique_queries.append(q)

        return unique_queries[:4]

    @classmethod
    def synthesize_grounded_response(
        cls,
        prompt: str,
        retrieved_sources: Sequence[tuple[str, str]],  # (url, content_chunk)
        target_brand: str,
    ) -> GllmGroundedResponse:
        """Synthesizes a citation-grounded response emulating modern GLLM search engines."""
        decomposed = cls.decompose_query(prompt, target_brand=target_brand)

        if not retrieved_sources:
            return GllmGroundedResponse(
                original_prompt=prompt,
                decomposed_queries=decomposed,
                synthesized_answer=f"No grounded sources retrieved for '{prompt}'.",
                citations=[],
                attribution_density=0.0,
            )

        citations: list[GroundedCitationAnchor] = []
        answer_clauses: list[str] = []

        for idx, (url, chunk) in enumerate(retrieved_sources[:3], start=1):
            # Take a concise 15-25 word excerpt for citation snippet
            words = chunk.strip().split()
            excerpt = " ".join(words[:20])
            citations.append(
                GroundedCitationAnchor(
                    citation_id=idx,
                    url=url,
                    snippet_preview=excerpt,
                )
            )
            # Create a grounded synthesized sentence with inline citation [idx]
            first_sentence = re.split(r"[.!?]", chunk)[0].strip()
            if first_sentence:
                answer_clauses.append(f"{first_sentence} [{idx}].")

        synthesized_text = " ".join(answer_clauses)
        total_words = len(synthesized_text.split())
        attr_density = round((len(citations) / max(1, total_words)) * 100.0, 2)

        return GllmGroundedResponse(
            original_prompt=prompt,
            decomposed_queries=decomposed,
            synthesized_answer=synthesized_text,
            citations=citations,
            attribution_density=attr_density,
        )

