"""Unit tests for Enterprise Technical SEO Audit Engine.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.seo.seo_audit_engine import SeoAuditEngine
from tests.test_config import (
    TARGET_BASE_URL,
    TEST_BROKEN_HTML,
    TEST_VALID_SEO_HTML,
)


def test_audit_page_high_score() -> None:
    html = TEST_VALID_SEO_HTML
    report = SeoAuditEngine.audit_page(html, url=TARGET_BASE_URL)

    assert report.overall_seo_score >= 90.0
    assert report.grade == "Excellent"
    assert report.title_valid is True
    assert report.meta_description_valid is True
    assert report.canonical_valid is True
    assert report.viewport_mobile_friendly is True
    assert report.heading_hierarchy_valid is True
    assert report.schema_org_valid is True
    assert len(report.detected_issues) == 0


def test_audit_page_missing_tags_detects_issues() -> None:
    broken_html = TEST_BROKEN_HTML
    report = SeoAuditEngine.audit_page(broken_html, url=TARGET_BASE_URL)

    assert report.overall_seo_score < 30.0
    assert report.grade == "Critical"
    assert report.title_valid is False
    assert report.meta_description_valid is False
    assert report.canonical_valid is False
    assert len(report.detected_issues) >= 4
    assert len(report.optimization_priorities) >= 3

