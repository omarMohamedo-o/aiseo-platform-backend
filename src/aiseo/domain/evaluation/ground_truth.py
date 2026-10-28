"""Domain models for real-world Ground Truth verification evidence."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GoogleSuggestEvidence(BaseModel):
    """Real search query suggestions from Google's official autocomplete engine."""

    model_config = ConfigDict(frozen=True)

    query: str
    suggestions: list[str] = Field(default_factory=list)
    has_brand_association: bool = False
    consensus_score: int = Field(ge=0, le=100)


class WikidataEntityEvidence(BaseModel):
    """Knowledge graph entity verification from Wikidata / Wikipedia."""

    model_config = ConfigDict(frozen=True)

    brand: str
    entity_found: bool = False
    wikidata_id: str | None = None
    label: str | None = None
    description: str | None = None
    official_website: str | None = None
    knowledge_graph_authority: int = Field(ge=0, le=100)


class DuckDuckGoEvidence(BaseModel):
    """Live AEO direct answer verification from DuckDuckGo Instant Answers."""

    model_config = ConfigDict(frozen=True)

    heading: str = ""
    abstract: str = ""
    source_url: str = ""
    has_direct_answer: bool = False
    concordance_score: int = Field(ge=0, le=100)


class GroundTruthValidationResult(BaseModel):
    """Complete multi-engine real-world ground truth verification report."""

    model_config = ConfigDict(frozen=True)

    domain: str
    brand: str
    timestamp: str
    google_search_evidence: GoogleSuggestEvidence
    wikidata_evidence: WikidataEntityEvidence
    duckduckgo_evidence: DuckDuckGoEvidence
    overall_empirical_confidence: int = Field(ge=0, le=100)
    verdict: str  # "HIGH_CONFIDENCE_GROUND_TRUTH" | "MODERATE_CONFIDENCE" | "EMERGING_ENTITY"
    methodology: str = "100% Free & Open-Source Empirical Verification (Google Suggest + Wikidata + DuckDuckGo)"

