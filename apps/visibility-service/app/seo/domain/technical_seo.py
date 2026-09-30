"""Domain models for Technical SEO audit data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CoreWebVitals(BaseModel):
    """Google Core Web Vitals metrics."""

    model_config = ConfigDict(extra="forbid")

    lcp_ms: float | None = None  # Largest Contentful Paint (milliseconds)
    cls_value: float | None = None  # Cumulative Layout Shift
    tbt_ms: float | None = None  # Total Blocking Time (milliseconds)


class TechnicalSeoAudit(BaseModel):
    """Technical SEO signals collected for a website.

    Aggregates PageSpeed scores, Core Web Vitals, and foundational
    technical checks (HTTPS, robots.txt, sitemap, etc.).
    """

    model_config = ConfigDict(extra="forbid")

    url: str

    # PageSpeed Scores (0-100)
    performance_score_mobile: float | None = None
    performance_score_desktop: float | None = None
    seo_score: float | None = None
    accessibility_score: float | None = None
    best_practices_score: float | None = None

    # Core Web Vitals
    mobile_vitals: CoreWebVitals | None = None
    desktop_vitals: CoreWebVitals | None = None

    # Technical Checks
    is_https: bool = False
    has_robots_txt: bool = False
    robots_txt_valid: bool = False
    has_sitemap: bool = False
    sitemap_valid: bool = False
    has_canonical: bool = False
    has_structured_data: bool = False
    structured_data_types: list[str] = []  # ["Organization", "Product", ...]
    has_hsts: bool = False
    redirect_chain_count: int = 0
    is_mobile_friendly: bool = False

    scanned_at: datetime | None = None
