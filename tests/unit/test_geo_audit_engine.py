"""Unit tests for Enterprise Generative Engine Optimization (GEO) Audit Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.geo.geo_audit_engine import GeoAuditEngine
from tests.test_config import (
    TARGET_BRAND,
    TARGET_DOMAIN,
    TEST_EVIDENCE_CHUNKS,
    TEST_VALID_AEO_HTML,
)


def test_geo_audit_market_leader() -> None:
    mentions = [True, True, True, True, True]  # 100% visibility
    responses = [
        f"{TARGET_BRAND} is a premier manufacturer of industrial on-site sodium hypochlorite electrochlorination systems. "
        f"{TARGET_BRAND} holds ISO 9001 certification and operates safely without chlorine gas deliveries."
    ]
    evidence = TEST_EVIDENCE_CHUNKS
    page_html = TEST_VALID_AEO_HTML

    report = GeoAuditEngine.evaluate(
        brand_name=TARGET_BRAND,
        domain=TARGET_DOMAIN,
        model_mentions=mentions,
        ai_responses=responses,
        crawled_evidence_chunks=evidence,
        page_html=page_html,
        citation_count=3,
    )

    assert report.overall_geo_index >= 75.0
    assert report.market_tier in ("Market Leader", "Challenger")
    assert report.factual_truth_score >= 80.0
    assert report.supported_claims_count >= 2
    assert report.contradicted_claims_count == 0
    assert TARGET_BRAND in report.strategic_summary


def test_geo_audit_low_visibility_tier() -> None:
    mentions = [False, False, False, False, True]  # 20% visibility
    responses = ["Other competitor systems dominate the municipal water market."]
    evidence = [f"{TARGET_BRAND} manufactures electrochlorination systems."]
    thin_html = "<html><body><p>Bare website.</p></body></html>"

    report = GeoAuditEngine.evaluate(
        brand_name=TARGET_BRAND,
        domain=TARGET_DOMAIN,
        model_mentions=mentions,
        ai_responses=responses,
        crawled_evidence_chunks=evidence,
        page_html=thin_html,
        citation_count=0,
    )

    assert report.overall_geo_index < 45.0
    assert report.market_tier in ("Emerging", "At Risk")
    assert len(report.actionable_remediations) > 0

