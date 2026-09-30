"""Crawler port definition."""
from __future__ import annotations

import abc

from aiseo.domain.value_objects import Url


class CrawlerPort(abc.ABC):
    """Interface for discovering pages on a website."""

    @abc.abstractmethod
    async def discover_pages(self, start_url: Url, max_pages: int = 10) -> list[Url]:
        """
        Crawl a website starting from the given URL and return a list of discovered URLs.
        
        Args:
            start_url: The entry point URL of the website.
            max_pages: Maximum number of pages to discover.
            
        Returns:
            A list of discovered internal URLs.
        """
