"""Trafilatura-based scraper adapter."""

from __future__ import annotations

import httpx
import trafilatura
from bs4 import BeautifulSoup

from aiseo.domain.value_objects import Url
from aiseo.domain.websites.page import ContentSection, StructuredContent
from aiseo.ports.scraper.scraper_port import ScraperPort


class TrafilaturaScraper(ScraperPort):
    def __init__(self, timeout: float = 15.0) -> None:
        self._timeout = timeout

    async def extract_content(self, url: Url) -> StructuredContent:
        async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
            response = await client.get(url.value)
            response.raise_for_status()
            html = response.text

        # Trafilatura for clean text
        extracted_text = trafilatura.extract(
            html, include_links=True, include_images=False, include_tables=True
        )
        if not extracted_text:
            extracted_text = ""

        # BeautifulSoup for title and basic sectioning (simplistic for MVP)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        html_tag = soup.html
        language = str(html_tag.get("lang")) if html_tag and html_tag.get("lang") else None

        # A very basic approach to create sections: split by double newlines from trafilatura
        # For a real implementation, we'd parse the markdown-like output from trafilatura or use soup headings
        sections = []
        if extracted_text:
            paragraphs = extracted_text.split("\n\n")
            current_heading: str | None = None
            current_content: list[str] = []

            for p in paragraphs:
                # Heuristic: if it's short and doesn't end with a period, it might be a heading
                if len(p) < 60 and not p.endswith(".") and not current_content:
                    current_heading = p
                else:
                    current_content.append(p)

                if len(current_content) > 3 or (
                    len(p) < 60 and not p.endswith(".") and current_content
                ):
                    sections.append(
                        ContentSection(
                            heading=current_heading, content="\n\n".join(current_content)
                        )
                    )
                    current_heading = None
                    current_content = []

            if current_content or current_heading:
                sections.append(
                    ContentSection(heading=current_heading, content="\n\n".join(current_content))
                )

        if not sections and extracted_text:
            sections = [ContentSection(heading=None, content=extracted_text)]

        return StructuredContent(
            title=title, language=language, sections=sections, raw_text=extracted_text
        )
