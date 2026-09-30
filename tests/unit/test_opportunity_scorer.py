"""Unit tests for OpportunityScorerService."""
from __future__ import annotations

from aiseo.application.reporting.opportunity_scorer import (
    OpportunityScorerService,
    calculate_opportunity_score,
)
from aiseo.domain.reporting.report_models import ReportKeyword


def test_calculate_opportunity_score_formula() -> None:
    # High volume, low difficulty, decent CPC
    kw = ReportKeyword(
        keyword="ai search optimization",
        volume="40,500",
        difficulty=20,
        cpc="$8.00",
        serp_features=4,
    )
    score = calculate_opportunity_score(kw)
    assert 70 <= score <= 100

    # Low volume, high difficulty, zero CPC
    low_kw = ReportKeyword(
        keyword="obscure query",
        volume="10",
        difficulty=95,
        cpc="$0.00",
        serp_features=0,
    )
    low_score = calculate_opportunity_score(low_kw)
    assert low_score < 20


def test_opportunity_scorer_service_alerts_on_shift() -> None:
    service = OpportunityScorerService()
    tenant = "tenant-1"

    kw_initial = [
        ReportKeyword(keyword="seo tool", volume="10,000", difficulty=60, cpc="$3.00", serp_features=2),
    ]
    scores1, alerts1 = service.score_keywords(tenant, kw_initial)
    assert len(scores1) == 1
    assert len(alerts1) == 0

    # Now difficulty drops drastically from 60 to 10 and volume doubles
    kw_shifted = [
        ReportKeyword(keyword="seo tool", volume="35,000", difficulty=10, cpc="$5.00", serp_features=4),
    ]
    scores2, alerts2 = service.score_keywords(tenant, kw_shifted)
    assert len(scores2) == 1
    assert len(alerts2) == 1  # Alert triggered on delta >= 10
    assert alerts2[0].delta >= 10
    assert alerts2[0].status == "open"

    # Acknowledge alert
    ack = service.acknowledge_alert(tenant, alerts2[0].id)
    assert ack is True
    all_alerts = service.get_alerts(tenant)
    assert all_alerts[0].status == "acknowledged"
