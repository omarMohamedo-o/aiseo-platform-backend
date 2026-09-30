"""Application service for analyzing a page's Answer Engine Optimization (AEO)."""

from __future__ import annotations

import re
import uuid

from apps.visibility_service.app.aeo.domain.citation_readiness import (
    AeoAudit,
    EntityGraph,
    FaqAnalysis,
)


class AeoAnalyzer:
    """Analyzes raw HTML and structural data to determine Citation Readiness."""

    def analyze_page(self, page_url: str, html_content: str, brand_name: str) -> AeoAudit:
        """Scan the HTML and determine how AEO-friendly the page is."""

        # 1. Analyze schema.org JSON-LD
        # (Very basic regex for MVP, in production use BeautifulSoup + json loads)
        has_faq_schema = '"@type": "FAQPage"' in html_content or '"@type":"FAQPage"' in html_content
        has_org_schema = (
            '"@type": "Organization"' in html_content or '"@type":"Organization"' in html_content
        )
        has_prod_schema = (
            '"@type": "Product"' in html_content or '"@type":"Product"' in html_content
        )

        # 2. Analyze Q&A structure visually
        # Look for headings containing question marks
        question_headings = re.findall(r"<h[2-4][^>]*>([^<]+\?)</h[2-4]>", html_content)
        qa_count = len(question_headings)

        # 3. Analyze general content structure
        has_lists = "<ul" in html_content or "<ol" in html_content
        has_headings = "<h2" in html_content

        # Entity mentions
        brand_count = html_content.lower().count(brand_name.lower())

        return AeoAudit(
            id=uuid.uuid4(),
            page_url=page_url,
            faq_data=FaqAnalysis(
                has_faq_schema=has_faq_schema,
                qa_pairs_detected=qa_count,
                # Assume concise if it has schema for now
                are_answers_concise=has_faq_schema,
            ),
            entity_data=EntityGraph(
                has_organization_schema=has_org_schema,
                has_product_schema=has_prod_schema,
                primary_entity_mentioned_count=brand_count,
            ),
            has_clear_headings=has_headings,
            has_bulleted_lists=has_lists,
        )
