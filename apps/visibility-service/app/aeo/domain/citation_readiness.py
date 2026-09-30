"""Domain models for Answer Engine Optimization (AEO) Analysis."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field


class FaqAnalysis(BaseModel):
    """Analysis of Frequently Asked Questions on a page."""

    has_faq_schema: bool = False
    qa_pairs_detected: int = 0
    are_answers_concise: bool = False  # e.g., < 50 words per answer


class EntityGraph(BaseModel):
    """How well the page establishes its core entities for knowledge graphs."""

    has_organization_schema: bool = False
    has_product_schema: bool = False
    primary_entity_mentioned_count: int = 0


class AeoAudit(BaseModel):
    """The result of an AEO scan for a specific page."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    page_url: str

    faq_data: FaqAnalysis = Field(default_factory=FaqAnalysis)
    entity_data: EntityGraph = Field(default_factory=EntityGraph)

    # Text structure signals
    has_clear_headings: bool = False
    has_bulleted_lists: bool = False

    def calculate_citation_readiness_score(self) -> int:
        """Calculate a 0-100 score indicating how easily an AI can cite this page."""
        score = 0

        # Schema is the strongest signal for AEO
        if self.faq_data.has_faq_schema:
            score += 30
        if self.entity_data.has_organization_schema:
            score += 15
        if self.entity_data.has_product_schema:
            score += 15

        # Content structure
        if self.faq_data.qa_pairs_detected > 0:
            score += 10
        if self.faq_data.are_answers_concise:
            score += 10
        if self.has_clear_headings:
            score += 10
        if self.has_bulleted_lists:
            score += 10

        return min(100, score)
