"""Scraper port definition."""

from __future__ import annotations

import abc

from aiseo.domain.value_objects import Url
from aiseo.domain.websites.page import StructuredContent


class ScraperPort(abc.ABC):
    """Interface for extracting and structuring content from a web page."""

    @abc.abstractmethod
    async def extract_content(self, url: Url) -> StructuredContent:
        """
        Download, parse, clean, and structure the content from the given URL.

        Args:
            url: The URL of the page to scrape.

        Returns:
            The structured content extracted from the page.
        """
