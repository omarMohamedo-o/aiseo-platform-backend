"""Reporting application services."""
from __future__ import annotations

from aiseo.application.reporting.opportunity_scorer import (
    OpportunityScorerService,
    calculate_opportunity_score,
)
from aiseo.application.reporting.report_generator import (
    ReportGeneratorService,
    generate_deterministic_summary,
)
from aiseo.application.reporting.scheduled_reports import (
    ScheduledReportsService,
    render_report_html,
)

__all__ = [
    "OpportunityScorerService",
    "ReportGeneratorService",
    "ScheduledReportsService",
    "calculate_opportunity_score",
    "generate_deterministic_summary",
    "render_report_html",
]
