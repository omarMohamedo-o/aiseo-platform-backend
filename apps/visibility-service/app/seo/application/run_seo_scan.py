"""Application service that orchestrates the full SEO scan pipeline.

This service ties together crawling, on-page analysis, SERP data
collection, score calculation, and recommendation generation into a
single use case: Run a complete SEO scan for a website.
"""

from __future__ import annotations

import uuid

from apps.visibility_service.app.seo.domain.page_seo_audit import PageSeoAudit
from apps.visibility_service.app.seo.domain.ports import (
    OnPageAnalyzer,
    PageSpeedProvider,
    SerpProvider,
)
from apps.visibility_service.app.seo.domain.scan_snapshot import (
    ScanSnapshot,
    ScoreBreakdown,
)
from apps.visibility_service.app.seo.domain.serp_result import SerpResult
from apps.visibility_service.app.seo.domain.technical_seo import TechnicalSeoAudit


class RunSeoScanService:
    """Orchestrates a full SEO scan for a client's website.

    Pipeline:
    1. Receive list of pages (from crawler-service, already crawled)
    2. Run OnPageAnalyzer on each page's HTML
    3. Run PageSpeedProvider on key pages
    4. Extract relevant keywords from content
    5. Run SerpProvider for each keyword
    6. Calculate SEO score
    7. Return ScanSnapshot

    This service depends only on Ports (Protocols), never on concrete
    adapters. Adapters are injected via the composition root.
    """

    def __init__(
        self,
        onpage_analyzer: OnPageAnalyzer,
        pagespeed_provider: PageSpeedProvider | None = None,
        serp_provider: SerpProvider | None = None,
    ) -> None:
        self._onpage = onpage_analyzer
        self._pagespeed = pagespeed_provider
        self._serp = serp_provider

    async def run_scan(
        self,
        website_id: uuid.UUID,
        tenant_id: uuid.UUID,
        target_domain: str,
        pages: list[dict[str, str]],  # [{"url": "...", "html": "..."}]
        keywords: list[str] | None = None,
        scan_number: int = 1,
    ) -> ScanSnapshot:
        """Execute a complete SEO scan and return a timestamped snapshot."""

        snapshot = ScanSnapshot.create(
            website_id=website_id,
            tenant_id=tenant_id,
            scan_number=scan_number,
        )
        snapshot = snapshot.start()

        # ── Step 1: On-Page Analysis ───────────────────────────
        page_audits: list[PageSeoAudit] = []
        for page in pages:
            audit = self._onpage.audit_page(url=page["url"], html=page["html"])
            page_audits.append(audit)

        # ── Step 2: Technical SEO (PageSpeed) ──────────────────
        technical_audit: TechnicalSeoAudit | None = None
        if self._pagespeed and pages:
            # Analyze the homepage (first URL)
            technical_audit = await self._pagespeed.analyze(url=pages[0]["url"], strategy="mobile")

        # ── Step 3: SERP Rankings ──────────────────────────────
        serp_results: list[SerpResult] = []
        if self._serp and keywords:
            serp_results = await self._serp.bulk_search(
                queries=keywords,
                target_domain=target_domain,
            )

        # ── Step 4: Calculate SEO Score ────────────────────────
        seo_score = self._calculate_seo_score(
            page_audits=page_audits,
            technical_audit=technical_audit,
            serp_results=serp_results,
        )

        # ── Step 5: Build final snapshot ───────────────────────
        snapshot = snapshot.complete(
            seo_score=seo_score,
            technical_audit=technical_audit or TechnicalSeoAudit(url=target_domain),
            page_audits=page_audits,
            serp_results=serp_results,
        )
        snapshot = snapshot.model_copy(update={"pages_crawled": len(pages)})

        return snapshot

    def _calculate_seo_score(
        self,
        page_audits: list[PageSeoAudit],
        technical_audit: TechnicalSeoAudit | None,
        serp_results: list[SerpResult],
    ) -> ScoreBreakdown:
        """Calculate the overall SEO score from all collected data.

        Scoring formula (weights configurable via Admin in Phase C):
        - Technical: 25% (PageSpeed, HTTPS, robots.txt, sitemap, etc.)
        - On-Page:   35% (meta tags, headings, images, links, schema)
        - Content:   20% (word count, keyword density, freshness)
        - Rankings:  20% (SERP positions for tracked keywords)
        """
        technical_score = self._score_technical(technical_audit)
        onpage_score = self._score_on_page(page_audits)
        content_score = self._score_content(page_audits)
        rankings_score = self._score_rankings(serp_results)

        overall = (
            technical_score * 0.25
            + onpage_score * 0.35
            + content_score * 0.20
            + rankings_score * 0.20
        )

        return ScoreBreakdown(
            overall=round(overall, 1),
            technical=round(technical_score, 1),
            on_page=round(onpage_score, 1),
            content=round(content_score, 1),
            rankings=round(rankings_score, 1),
        )

    def _score_technical(self, audit: TechnicalSeoAudit | None) -> float:
        if audit is None:
            return 50.0  # Default when PageSpeed not available

        score = 0.0
        checks = 0

        # PageSpeed scores
        if audit.performance_score_mobile is not None:
            score += audit.performance_score_mobile
            checks += 1

        # Boolean checks (each worth 10 points)
        booleans = [
            audit.is_https,
            audit.has_robots_txt,
            audit.has_sitemap,
            audit.has_canonical,
            audit.has_structured_data,
            audit.is_mobile_friendly,
        ]
        bool_score = sum(10.0 for b in booleans if b)
        total_bool = len(booleans) * 10.0

        if checks > 0:
            return (score / checks * 0.6) + (bool_score / total_bool * 100 * 0.4)
        return bool_score / total_bool * 100

    def _score_on_page(self, audits: list[PageSeoAudit]) -> float:
        if not audits:
            return 0.0

        page_scores: list[float] = []
        for audit in audits:
            s = 0.0
            total = 0.0

            # Title tag (20 points)
            total += 20
            if audit.meta.title:
                s += 10
                if 30 <= audit.meta.title_length <= 60:
                    s += 10

            # Meta description (20 points)
            total += 20
            if audit.meta.meta_description:
                s += 10
                if 120 <= audit.meta.meta_description_length <= 160:
                    s += 10

            # Headings (15 points)
            total += 15
            if audit.headings.h1_count == 1:
                s += 10
            if audit.headings.hierarchy_valid:
                s += 5

            # Images (15 points)
            total += 15
            coverage = audit.images.alt_coverage_pct
            s += coverage / 100 * 15

            # Links (10 points)
            total += 10
            if audit.links.internal_link_count > 0:
                s += 5
            if audit.links.broken_link_count == 0:
                s += 5

            # Structured data (10 points)
            total += 10
            if audit.structured_data.has_json_ld:
                s += 7
            if audit.structured_data.has_microdata:
                s += 3

            # Open Graph (10 points)
            total += 10
            if audit.meta.has_open_graph:
                s += 10

            page_scores.append((s / total) * 100 if total > 0 else 0)

        return sum(page_scores) / len(page_scores)

    def _score_content(self, audits: list[PageSeoAudit]) -> float:
        if not audits:
            return 0.0

        scores: list[float] = []
        for audit in audits:
            s = 0.0
            # Word count scoring
            if audit.word_count >= 1500:
                s += 40
            elif audit.word_count >= 800:
                s += 30
            elif audit.word_count >= 300:
                s += 20
            else:
                s += 5  # Thin content penalty

            # Language detected
            if audit.language:
                s += 10

            # Has structured headings
            if audit.headings.h2_count > 0:
                s += 25
            if audit.headings.h3_count > 0:
                s += 15

            # Keyword presence
            if audit.keyword_density and 1.0 <= audit.keyword_density <= 3.0:
                s += 10

            scores.append(min(s, 100))

        return sum(scores) / len(scores)

    def _score_rankings(self, results: list[SerpResult]) -> float:
        if not results:
            return 50.0  # Default when SERP not available

        position_scores: list[float] = []
        for result in results:
            if result.position is None:
                position_scores.append(0)  # Not ranked = 0
            elif result.position <= 3:
                position_scores.append(100)
            elif result.position <= 10:
                position_scores.append(80)
            elif result.position <= 20:
                position_scores.append(60)
            elif result.position <= 50:
                position_scores.append(30)
            else:
                position_scores.append(10)

        return sum(position_scores) / len(position_scores)
