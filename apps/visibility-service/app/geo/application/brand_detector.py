"""Application service for detecting brand mentions in LLM text."""

from __future__ import annotations

import re

from apps.visibility_service.app.geo.domain.geo_simulation import BrandMention


class BrandDetector:
    """Analyzes raw LLM text to detect if a specific brand is mentioned.

    For MVP, we use a regex/keyword-based approach. In V2, we could use
    a small classification LLM to determine sentiment and exact ranking.
    """

    def analyze(self, raw_text: str, target_brand: str) -> BrandMention:
        """Scan the text for the brand and determine visibility."""

        # Simple case-insensitive exact match
        text_lower = raw_text.lower()
        brand_lower = target_brand.lower()

        mentioned = brand_lower in text_lower

        # Determine sentiment (MVP placeholder heuristic)
        sentiment = "NONE"
        if mentioned:
            # Very naive check for negative sentiment words near the brand
            # In a real app, use an NLP library or zero-shot classifier here
            if re.search(rf"\b(bad|terrible|avoid)\b.*\b{re.escape(brand_lower)}\b", text_lower):
                sentiment = "NEGATIVE"
            elif re.search(
                rf"\b(best|excellent|recommend)\b.*\b{re.escape(brand_lower)}\b", text_lower
            ):
                sentiment = "POSITIVE"
            else:
                sentiment = "NEUTRAL"

        # Determine rank position (e.g. "1. BrandName")
        rank = None
        if mentioned:
            match = re.search(rf"(\d+)[\.\)]\s*(?:\*\*)?{re.escape(brand_lower)}", text_lower)
            if match:
                try:
                    rank = int(match.group(1))
                except ValueError:
                    pass

        return BrandMention(
            brand_name=target_brand,
            mentioned=mentioned,
            sentiment=sentiment,
            rank_position=rank,
        )
