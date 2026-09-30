"""Port interfaces for SEO data collection.

These Protocols define how the visibility-service collects SEO data.
Concrete adapters (DataForSEO, Serper, GooglePageSpeed, etc.) implement
these through composition, never inheritance.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from apps.visibility_service.app.seo.domain.page_seo_audit import PageSeoAudit
from apps.visibility_service.app.seo.domain.serp_result import SerpResult
from apps.visibility_service.app.seo.domain.technical_seo import TechnicalSeoAudit


@runtime_checkable
class SerpProvider(Protocol):
    """Fetches search engine ranking data for keywords."""

    async def search(self, query: str, target_domain: str, location: str = "US") -> SerpResult:
        """Search for a single query and return ranking data."""
        ...

    async def bulk_search(
        self, queries: list[str], target_domain: str, location: str = "US"
    ) -> list[SerpResult]:
        """Search for multiple queries at once."""
        ...


@runtime_checkable
class PageSpeedProvider(Protocol):
    """Fetches technical SEO and performance data using Google PageSpeed."""

    async def analyze(self, url: str, strategy: str = "mobile") -> TechnicalSeoAudit:
        """Analyze a URL and return technical SEO metrics."""
        ...


@runtime_checkable
class OnPageAnalyzer(Protocol):
    """Analyzes raw HTML to extract on-page SEO signals."""

    def audit_page(self, url: str, html: str) -> PageSeoAudit:
        """Audit a single page's HTML for on-page SEO factors."""
        ...
