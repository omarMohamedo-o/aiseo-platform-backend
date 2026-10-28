"""Trafilatura-based scraper adapter."""
from __future__ import annotations

import json
from urllib.parse import urlparse

import httpx
import structlog
import trafilatura
from bs4 import BeautifulSoup

from aiseo.application.nlp.arabic_normalizer import ArabicNormalizer
from aiseo.domain.value_objects import Url
from aiseo.domain.websites.page import ContentSection, StructuredContent
from aiseo.ports.scraper.scraper_port import ScraperPort

logger = structlog.get_logger(__name__)


class TrafilaturaScraper(ScraperPort):
    def __init__(self, timeout: float = 15.0) -> None:
        self._timeout = timeout

    async def extract_content(self, url: Url) -> StructuredContent:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AISEO-Scraper/2.0 (compatible; Enterprise Audit Engine)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True, headers=headers) as client:
            response = await client.get(url.value)
            response.raise_for_status()
            html = response.text

        # 1. Primary: Trafilatura for clean text
        extracted_text = trafilatura.extract(
            html,
            include_links=True,
            include_images=False,
            include_tables=True,
            favor_precision=False,
        )
        if not extracted_text:
            extracted_text = ""

        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        html_tag = soup.html
        language = str(html_tag.get("lang")) if html_tag and html_tag.get("lang") else "en"

        # 2. Intelligent Fallback: If body text is sparse or client-side SPA (<div id="root">)
        if len(extracted_text.strip()) < 80:
            parts: list[str] = []

            # Page topic derived from URL path slug
            path = urlparse(url.value).path.strip("/")
            slug_topic = path.replace("-", " ").replace("/", " - ").title() if path else "Homepage"
            parts.append(f"Section Topic: {slug_topic}")

            if title:
                parts.append(f"Page Title: {title}")

            # Meta Description / OG Description
            desc_meta = (
                soup.find("meta", attrs={"name": "description"})
                or soup.find("meta", attrs={"property": "og:description"})
                or soup.find("meta", attrs={"name": "twitter:description"})
            )
            if desc_meta:
                raw_desc = desc_meta.get("content")
                if raw_desc:
                    desc_str = (" ".join(raw_desc) if isinstance(raw_desc, list) else raw_desc).strip()
                    if desc_str:
                        parts.append(f"Executive Summary: {desc_str}")

            # Meta Keywords
            kw_meta = soup.find("meta", attrs={"name": "keywords"})
            if kw_meta:
                raw_kw = kw_meta.get("content")
                if raw_kw:
                    kw_str = (" ".join(raw_kw) if isinstance(raw_kw, list) else raw_kw).strip()
                    if kw_str:
                        parts.append(f"Core Keywords: {kw_str}")

            # JSON-LD Structured Data
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    if isinstance(data, dict):
                        entity_name = data.get("name") or data.get("headline")
                        overview = data.get("description") or data.get("about")
                        if entity_name:
                            parts.append(f"Entity: {entity_name}")
                        if overview:
                            parts.append(f"Overview: {overview}")
                        if "contactPoint" in data and isinstance(data["contactPoint"], dict):
                            cp = data["contactPoint"]
                            parts.append(f"Contact Support: {cp.get('telephone', '')} {cp.get('email', '')}".strip())
                except Exception:
                    pass

            # Headings
            headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) if h.get_text(strip=True)]
            if headings:
                parts.append("Headings: " + " | ".join(headings[:10]))

            # Meaningful list items
            list_items = [li.get_text(strip=True) for li in soup.find_all("li") if len(li.get_text(strip=True)) > 15]
            if list_items:
                parts.append("Key Offerings: " + "; ".join(list_items[:8]))

            extracted_text = "\n\n".join(parts)

        # Normalize Arabic text and numerals if present (preserves clean English text untouched)
        if extracted_text and ArabicNormalizer.is_arabic(extracted_text):
            extracted_text = ArabicNormalizer.normalize(extracted_text)

        if title and ArabicNormalizer.is_arabic(title):
            title = ArabicNormalizer.normalize(title)

        # 3. Create structured content sections
        sections: list[ContentSection] = []
        if extracted_text:
            paragraphs = [p.strip() for p in extracted_text.split("\n\n") if p.strip()]
            for p in paragraphs:
                sections.append(ContentSection(heading=None, content=p))

        if not sections and extracted_text:
            sections = [ContentSection(heading=None, content=extracted_text)]

        return StructuredContent(
            title=title,
            language=language,
            sections=sections,
            raw_text=extracted_text,
            raw_html=html,
        )

