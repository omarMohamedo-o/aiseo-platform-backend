"""On-page SEO analyzer using BeautifulSoup.

Extracts all on-page SEO signals from raw HTML: meta tags, headings,
images, links, structured data, and content metrics. This adapter
implements the OnPageAnalyzer port and has zero domain dependencies.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from urllib.parse import urljoin, urlparse

from apps.visibility_service.app.seo.domain.page_seo_audit import (
    HeadingInfo,
    ImageInfo,
    LinkInfo,
    MetaTagInfo,
    PageSeoAudit,
    StructuredDataInfo,
)
from bs4 import BeautifulSoup, Tag


class HtmlOnPageAnalyzer:
    """Analyzes raw HTML to extract comprehensive on-page SEO data.

    Satisfies the OnPageAnalyzer Protocol structurally (duck typing).
    BeautifulSoup is an internal implementation detail, never exposed.
    """

    def audit_page(self, url: str, html: str) -> PageSeoAudit:
        """Audit a single page's HTML and return all on-page SEO data."""
        soup = BeautifulSoup(html, "lxml")
        parsed_url = urlparse(url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return PageSeoAudit(
            url=url,
            word_count=self._count_words(soup),
            language=self._extract_language(soup),
            meta=self._extract_meta_tags(soup),
            headings=self._extract_headings(soup),
            links=self._extract_links(soup, base_domain),
            images=self._extract_images(soup),
            structured_data=self._extract_structured_data(soup),
            scanned_at=datetime.now(UTC),
        )

    # ── Meta Tags ──────────────────────────────────────────────

    def _extract_meta_tags(self, soup: BeautifulSoup) -> MetaTagInfo:
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else None

        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc_content = str(meta_desc.get("content", "")) if meta_desc else None

        canonical = soup.find("link", attrs={"rel": "canonical"})
        canonical_url = str(canonical.get("href", "")) if canonical else None

        robots_meta = soup.find("meta", attrs={"name": "robots"})
        robots_content = str(robots_meta.get("content", "")) if robots_meta else None

        # Open Graph
        og_title_tag = soup.find("meta", attrs={"property": "og:title"})
        og_desc_tag = soup.find("meta", attrs={"property": "og:description"})
        og_image_tag = soup.find("meta", attrs={"property": "og:image"})

        # Twitter Card
        twitter_card = soup.find("meta", attrs={"name": "twitter:card"})

        return MetaTagInfo(
            title=title_text,
            title_length=len(title_text) if title_text else 0,
            meta_description=desc_content,
            meta_description_length=len(desc_content) if desc_content else 0,
            has_canonical=canonical is not None,
            canonical_url=canonical_url,
            has_robots_meta=robots_meta is not None,
            robots_content=robots_content,
            has_open_graph=og_title_tag is not None,
            og_title=(str(og_title_tag.get("content", "")) if og_title_tag else None),
            og_description=(str(og_desc_tag.get("content", "")) if og_desc_tag else None),
            og_image=(str(og_image_tag.get("content", "")) if og_image_tag else None),
            has_twitter_card=twitter_card is not None,
        )

    # ── Headings ───────────────────────────────────────────────

    def _extract_headings(self, soup: BeautifulSoup) -> HeadingInfo:
        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")

        h1_texts = [tag.get_text(strip=True) for tag in h1_tags]

        # Check hierarchy validity: H1 should come before H2, H2 before H3
        hierarchy_valid = self._check_heading_hierarchy(soup)

        return HeadingInfo(
            h1_count=len(h1_tags),
            h1_texts=h1_texts,
            h2_count=len(h2_tags),
            h3_count=len(h3_tags),
            hierarchy_valid=hierarchy_valid,
        )

    def _check_heading_hierarchy(self, soup: BeautifulSoup) -> bool:
        """Check if heading tags follow a logical hierarchy (H1 → H2 → H3)."""
        headings = soup.find_all(re.compile(r"^h[1-6]$"))
        if not headings:
            return False

        prev_level = 0
        for heading in headings:
            level = int(heading.name[1])
            # A heading should not skip more than one level down
            if level > prev_level + 1 and prev_level > 0:
                return False
            prev_level = level

        # Must have exactly one H1
        h1_count = len(soup.find_all("h1"))
        return h1_count == 1

    # ── Links ──────────────────────────────────────────────────

    def _extract_links(self, soup: BeautifulSoup, base_domain: str) -> LinkInfo:
        all_links = soup.find_all("a", href=True)
        internal_count = 0
        external_count = 0
        nofollow_count = 0

        for link in all_links:
            href = str(link.get("href", ""))
            rel = str(link.get("rel", ""))

            if "nofollow" in rel:
                nofollow_count += 1

            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue

            full_url = urljoin(base_domain, href)
            if urlparse(full_url).netloc == urlparse(base_domain).netloc:
                internal_count += 1
            else:
                external_count += 1

        return LinkInfo(
            internal_link_count=internal_count,
            external_link_count=external_count,
            broken_link_count=0,  # Requires HTTP requests, done separately
            nofollow_count=nofollow_count,
        )

    # ── Images ─────────────────────────────────────────────────

    def _extract_images(self, soup: BeautifulSoup) -> ImageInfo:
        all_images = soup.find_all("img")
        with_alt = 0
        without_alt = 0
        images_without_alt: list[str] = []

        for img in all_images:
            alt = img.get("alt")
            src = str(img.get("src", ""))

            if alt and str(alt).strip():
                with_alt += 1
            else:
                without_alt += 1
                if src:
                    images_without_alt.append(src)

        return ImageInfo(
            total_count=len(all_images),
            with_alt_count=with_alt,
            without_alt_count=without_alt,
            images_without_alt=images_without_alt[:20],  # Cap at 20
        )

    # ── Structured Data ────────────────────────────────────────

    def _extract_structured_data(self, soup: BeautifulSoup) -> StructuredDataInfo:
        # JSON-LD blocks
        json_ld_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        json_ld_blocks: list[dict] = []  # type: ignore[type-arg]
        schema_types: list[str] = []
        validation_errors: list[str] = []

        for script in json_ld_scripts:
            text = script.get_text(strip=True)
            if text:
                try:
                    data = json.loads(text)
                    json_ld_blocks.append(data)
                    # Extract @type
                    if isinstance(data, dict) and "@type" in data:
                        schema_types.append(str(data["@type"]))
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and "@type" in item:
                                schema_types.append(str(item["@type"]))
                except json.JSONDecodeError as e:
                    validation_errors.append(f"Invalid JSON-LD: {e}")

        # Microdata check
        has_microdata = bool(
            soup.find(attrs={"itemscope": True}) or soup.find(attrs={"itemtype": True})
        )

        return StructuredDataInfo(
            has_json_ld=len(json_ld_blocks) > 0,
            has_microdata=has_microdata,
            schema_types=schema_types,
            json_ld_blocks=json_ld_blocks,
            validation_errors=validation_errors,
        )

    # ── Content Metrics ────────────────────────────────────────

    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in the visible text content."""
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        text = soup.get_text(separator=" ", strip=True)
        words = text.split()
        return len(words)

    def _extract_language(self, soup: BeautifulSoup) -> str | None:
        """Extract the page language from the html tag."""
        html_tag = soup.find("html")
        if html_tag and isinstance(html_tag, Tag):
            lang = html_tag.get("lang")
            if lang:
                return str(lang)
        return None
