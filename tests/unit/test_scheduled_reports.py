"""Unit tests for ScheduledReportsService and HTML email rendering."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aiseo.application.reporting.opportunity_scorer import OpportunityScorerService
from aiseo.application.reporting.report_generator import ReportGeneratorService
from aiseo.application.reporting.scheduled_reports import (
    ScheduledReportsService,
    render_report_html,
)
from aiseo.domain.reporting.report_models import (
    OpportunityScore,
    ReportBranding,
    ReportKeyword,
    ReportSummary,
)
from aiseo.ports.notifications.email_port import EmailPort


def test_render_report_html_structure() -> None:
    branding = ReportBranding(company_name="Acme Corp", accent_color="#ff5500")
    summary = ReportSummary(
        headline="Strong AI Overview Presence",
        summary="Acme Corp gained significant ground in answer engine search results.",
        insights=["Insight 1", "Insight 2"],
        actions=["Action 1", "Action 2"],
    )
    scores = [
        OpportunityScore(keyword="geo search", score=88, volume="12,000", difficulty=25, cpc="$4.00", serp_features=3)
    ]

    html = render_report_html(summary, "Weekly Audit", branding, scores)
    assert "Acme Corp" in html
    assert "#ff5500" in html
    assert "Strong AI Overview Presence" in html
    assert "geo search" in html
    assert "88/100" in html


@pytest.mark.asyncio
async def test_scheduled_reports_service_workflow() -> None:
    mock_email = AsyncMock(spec=EmailPort)
    mock_email.send_email.return_value = True

    scorer = OpportunityScorerService()
    generator = ReportGeneratorService(llm_provider=None)
    service = ScheduledReportsService(
        email_adapter=mock_email,
        report_generator=generator,
        opportunity_scorer=scorer,
    )

    tenant = "tenant-100"

    # Save custom branding
    service.save_branding(
        tenant,
        ReportBranding(company_name="Vanguard AI", accent_color="#00aa88"),
    )

    # Create schedule
    sched = service.create_schedule(
        tenant_id=tenant,
        name="Monday Executive Brief",
        cron="0 9 * * 1",
        recipient_email="leadership@vanguard.ai",
        tone="executive",
        keywords=[
            ReportKeyword(keyword="enterprise seo", volume="15,000", difficulty=40, cpc="$5.00", serp_features=3)
        ],
    )

    assert sched.name == "Monday Executive Brief"
    assert sched.recipient_email == "leadership@vanguard.ai"

    # Execute scheduled run
    success = await service.execute_report_run(tenant, sched.id)
    assert success is True
    assert mock_email.send_email.call_count == 1

    call_args = mock_email.send_email.call_args[1]
    assert call_args["to"] == ["leadership@vanguard.ai"]
    assert "Vanguard AI" in call_args["subject"]
    assert "Vanguard AI" in call_args["html"]
