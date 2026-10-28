"""Enterprise Technical SEO Audit Engine.

Evaluates classical search engine optimization parameters including metadata integrity,
canonicalization, heading hierarchies, Schema.org structure, and internal link equity.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from aiseo.application.seo.schema_validator import SchemaValidator


@dataclass(frozen=True)
class SeoAuditReport:
    """Consolidated technical SEO assessment report."""
    overall_seo_score: float  # Scale 0 - 100
    grade: str  # Excellent / Good / Needs Improvement / Critical
    title_valid: bool
    title_text: str | None
    meta_description_valid: bool
    meta_description_text: str | None
    canonical_valid: bool
    viewport_mobile_friendly: bool
    heading_hierarchy_valid: bool
    schema_org_valid: bool
    word_count: int
    detected_issues: list[str]
    optimization_priorities: list[str]


class SeoAuditEngine:
    """Deterministic classical SEO evaluation engine."""

    @classmethod
    def audit_page(cls, html_content: str, url: str) -> SeoAuditReport:
        """Performs a comprehensive technical SEO audit of crawled HTML."""
        if not html_content:
            return SeoAuditReport(
                overall_seo_score=0.0,
                grade="Critical",
                title_valid=False,
                title_text=None,
                meta_description_valid=False,
                meta_description_text=None,
                canonical_valid=False,
                viewport_mobile_friendly=False,
                heading_hierarchy_valid=False,
                schema_org_valid=False,
                word_count=0,
                detected_issues=["Empty or unparseable HTML content"],
                optimization_priorities=["Provide accessible HTML page content"],
            )

        issues: list[str] = []
        priorities: list[str] = []
        score = 0.0

        # 1. Page Title Tag (Optimal 30-65 chars)
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
        title_text = title_match.group(1).strip() if title_match else None
        title_valid = False
        if title_text:
            t_len = len(title_text)
            if 30 <= t_len <= 65:
                title_valid = True
                score += 20.0
            elif t_len > 65:
                issues.append(f"Title is too long ({t_len} chars, exceeds 65 char truncation limit).")
                score += 12.0
            else:
                issues.append(f"Title is too short ({t_len} chars, under 30 char minimum).")
                score += 10.0
        else:
            issues.append("Missing <title> tag.")
            priorities.append("Add descriptive 30-65 character <title> tag.")

        # 2. Meta Description Tag (Optimal 70-160 chars)
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html_content, re.IGNORECASE)
        desc_text = desc_match.group(1).strip() if desc_match else None
        meta_desc_valid = False
        if desc_text:
            d_len = len(desc_text)
            if 70 <= d_len <= 160:
                meta_desc_valid = True
                score += 20.0
            elif d_len > 160:
                issues.append(f"Meta description exceeds 160 chars ({d_len} chars).")
                score += 12.0
            else:
                issues.append(f"Meta description is too short ({d_len} chars, under 70 char minimum).")
                score += 10.0
        else:
            issues.append("Missing meta description.")
            priorities.append("Add high-converting 70-160 character meta description.")

        # 3. Canonical Tag
        canonical_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html_content, re.IGNORECASE)
        canonical_valid = bool(canonical_match)
        if canonical_valid:
            score += 15.0
        else:
            issues.append("Missing rel='canonical' tag (risk of duplicate content penalties).")
            priorities.append("Specify self-referential or authoritative canonical URL.")

        # 4. Viewport Mobile-Friendliness
        viewport_match = re.search(r'<meta[^>]+name=["\']viewport["\']', html_content, re.IGNORECASE)
        viewport_valid = bool(viewport_match)
        if viewport_valid:
            score += 15.0
        else:
            issues.append("Missing mobile viewport meta tag.")
            priorities.append("Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>.")

        # 5. Heading Hierarchy (Strict single H1 + at least one H2)
        h1_matches = len(re.findall(r"<h1\b", html_content, re.IGNORECASE))
        h2_matches = len(re.findall(r"<h2\b", html_content, re.IGNORECASE))
        heading_valid = (h1_matches == 1 and h2_matches >= 1)
        if heading_valid:
            score += 15.0
        elif h1_matches == 0:
            issues.append("Missing <h1> main headline.")
            priorities.append("Include exactly one descriptive <h1> headline.")
        elif h1_matches > 1:
            issues.append(f"Multiple <h1> tags detected ({h1_matches} found; standards recommend exactly 1).")
            score += 8.0
        else:
            issues.append("No <h2> subheadings found.")
            score += 8.0

        # 6. Schema.org JSON-LD Structured Data
        jsonld_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
        schema_valid = False
        if jsonld_matches:
            for snippet in jsonld_matches:
                val_res = SchemaValidator.validate_jsonld(snippet.strip())
                if val_res.is_valid:
                    schema_valid = True
                    break
        if schema_valid:
            score += 15.0
        else:
            issues.append("No valid Schema.org JSON-LD structured data detected.")
            priorities.append("Inject validated Schema.org JSON-LD markup.")

        # Text length check
        body_text = re.sub(r"<[^>]+>", " ", html_content)
        words = len(re.findall(r"\b\w+\b", body_text))

        final_score = round(min(100.0, score), 1)

        if final_score >= 85.0:
            grade = "Excellent"
        elif final_score >= 65.0:
            grade = "Good"
        elif final_score >= 45.0:
            grade = "Needs Improvement"
        else:
            grade = "Critical"

        return SeoAuditReport(
            overall_seo_score=final_score,
            grade=grade,
            title_valid=title_valid,
            title_text=title_text,
            meta_description_valid=meta_desc_valid,
            meta_description_text=desc_text,
            canonical_valid=canonical_valid,
            viewport_mobile_friendly=viewport_valid,
            heading_hierarchy_valid=heading_valid,
            schema_org_valid=schema_valid,
            word_count=words,
            detected_issues=issues,
            optimization_priorities=priorities,
        )

