"""API routes for reports, opportunity scores, and email schedules."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import (
    get_opportunity_scorer_service,
    get_report_generator_service,
    get_scheduled_reports_service,
)
from aiseo.application.reporting.opportunity_scorer import OpportunityScorerService
from aiseo.application.reporting.report_generator import ReportGeneratorService
from aiseo.application.reporting.scheduled_reports import ScheduledReportsService
from aiseo.domain.reporting.report_models import (
    OpportunityScore,
    ReportBranding,
    ReportKeyword,
    ReportSchedule,
    ReportSummary,
    ReportToneType,
)

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


def _extract_tenant(x_tenant_id: str | None = Header(default="default-tenant")) -> str:
    return x_tenant_id or "default-tenant"


class KeywordSummaryRequest(BaseModel):
    keywords: list[ReportKeyword] = Field(default_factory=list)
    trend_points: list[dict[str, Any]] | None = None
    tone: ReportToneType = "executive"


class KeywordSummaryResponse(BaseModel):
    summary: ReportSummary
    scores: list[OpportunityScore]
    headline: str
    summary_text: str
    insights: list[str]
    actions: list[str]
    confidence: str
    model: str
    scored_keywords: list[ReportKeyword]


class CreateScheduleRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    cron: str = "0 9 * * 1"  # Every Monday at 9am
    recipient_email: str = Field(min_length=5, max_length=320)
    tone: ReportToneType = "executive"
    keywords: list[ReportKeyword] = Field(default_factory=list)


class SendTestEmailRequest(BaseModel):
    recipient_email: str
    tone: ReportToneType = "executive"
    keywords: list[ReportKeyword] | None = None


@router.post("/summary", response_model=KeywordSummaryResponse)
async def generate_keyword_summary(
    payload: KeywordSummaryRequest,
    tenant_id: str = Depends(_extract_tenant),
    scorer: OpportunityScorerService = Depends(get_opportunity_scorer_service),
    generator: ReportGeneratorService = Depends(get_report_generator_service),
) -> KeywordSummaryResponse:
    # 1. Calculate Opportunity Scores entirely on backend
    scores, _ = scorer.score_keywords(tenant_id, payload.keywords)
    # 2. Generate narrative summary
    summary = await generator.generate_summary(
        keywords=payload.keywords,
        trend_points=payload.trend_points,
        tone=payload.tone,
    )

    # Attach computed scores to scored_keywords
    score_map = {s.keyword: s.score for s in scores}
    scored_kw_list = [
        kw.model_copy(update={"score": score_map.get(kw.keyword, 50)})
        for kw in payload.keywords
    ]

    return KeywordSummaryResponse(
        summary=summary,
        scores=scores,
        headline=summary.headline,
        summary_text=summary.summary,
        insights=summary.insights,
        actions=summary.actions,
        confidence="high",
        model=summary.model,
        scored_keywords=scored_kw_list,
    )


@router.get("/branding", response_model=ReportBranding)
async def get_branding(
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> ReportBranding:
    return service.get_branding(tenant_id)


@router.post("/branding", response_model=ReportBranding)
async def save_branding(
    payload: ReportBranding,
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> ReportBranding:
    return service.save_branding(tenant_id, payload)


@router.get("/schedules", response_model=list[ReportSchedule])
async def list_schedules(
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> list[ReportSchedule]:
    return service.list_schedules(tenant_id)


@router.post("/schedules", response_model=ReportSchedule)
async def create_schedule(
    payload: CreateScheduleRequest,
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> ReportSchedule:
    return service.create_schedule(
        tenant_id=tenant_id,
        name=payload.name,
        cron=payload.cron,
        recipient_email=payload.recipient_email,
        tone=payload.tone,
        keywords=payload.keywords,
    )


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> dict[str, bool]:
    success = service.delete_schedule(tenant_id, schedule_id)
    return {"success": success}


@router.post("/send-test")
async def send_test_email(
    payload: SendTestEmailRequest,
    tenant_id: str = Depends(_extract_tenant),
    service: ScheduledReportsService = Depends(get_scheduled_reports_service),
) -> dict[str, bool]:
    success = await service.send_test_report(
        tenant_id=tenant_id,
        recipient_email=payload.recipient_email,
        tone=payload.tone,
        keywords=payload.keywords,
    )
    return {"success": success}
