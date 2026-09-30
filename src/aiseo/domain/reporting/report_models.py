"""Domain models for reports, opportunity scores, and scheduled email alerts."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReportToneType = Literal["executive", "technical", "content-strategy"]


class ReportBranding(BaseModel):
    """Custom corporate branding applied to outgoing email and PDF reports."""

    model_config = ConfigDict(frozen=True)

    company_name: str = "SignalOS"
    logo_url: str | None = None
    accent_color: str = "#1689e8"
    footer_text: str = "SignalOS · AI visibility intelligence"


class ReportKeyword(BaseModel):
    """Keyword input row used for opportunity scoring and reporting."""

    model_config = ConfigDict(frozen=True)

    keyword: str
    intent: str = "informational"
    volume: str = "0"
    difficulty: str | int | float = 0
    cpc: str = "$0.00"
    serp_features: str | int = 0


class OpportunityScore(BaseModel):
    """Calculated opportunity score for a target keyword."""

    model_config = ConfigDict(frozen=True)

    keyword: str
    score: int = Field(ge=0, le=100)
    volume: str
    difficulty: float
    cpc: str
    serp_features: int


class OpportunityAlert(BaseModel):
    """Alert triggered when an opportunity score shifts significantly."""

    model_config = ConfigDict(frozen=True)

    id: str
    tenant_id: str
    keyword: str
    previous_score: int
    current_score: int
    delta: int
    threshold: int = 10
    status: Literal["open", "acknowledged"] = "open"


class ReportSummary(BaseModel):
    """Executive narrative summary generated for a visibility report."""

    model_config = ConfigDict(frozen=True)

    headline: str
    summary: str
    insights: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    model: str = "deterministic"


class ReportSchedule(BaseModel):
    """Configuration for recurring automated email report delivery."""

    model_config = ConfigDict(frozen=True)

    id: str
    tenant_id: str
    name: str
    cron: str
    recipient_email: str
    tone: ReportToneType = "executive"
    enabled: bool = True
    branding: ReportBranding = Field(default_factory=ReportBranding)
    keywords: list[ReportKeyword] = Field(default_factory=list)
