"""httpx-based crawler adapter."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from aiseo.domain.value_objects import Url
from aiseo.ports.crawler.crawler_port import CrawlerPort


class HttpxCrawler(CrawlerPort):
    def __init__(self, timeout: float = 10.0) -> None:
        self._timeout = timeout

    async def discover_pages(self, start_url: Url, max_pages: int = 10) -> list[Url]:
        discovered: set[str] = set()
        to_visit = [start_url.value]
        base_domain = urlparse(start_url.value).netloc

        async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
            while to_visit and len(discovered) < max_pages:
                current_url = to_visit.pop(0)
                if current_url in discovered:
                    continue

                try:
                    response = await client.get(current_url)
                    response.raise_for_status()

                    discovered.add(current_url)

                    if "text/html" in response.headers.get("content-type", ""):
                        soup = BeautifulSoup(response.content, "html.parser")
                        for a_tag in soup.find_all("a", href=True):
                            href = str(a_tag["href"])
                            absolute_url = urljoin(str(current_url), href)
                            parsed = urlparse(absolute_url)

                            # Only stay within the same domain, ignore fragments
                            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                            if (
                                parsed.netloc == base_domain
                                and clean_url not in discovered
                                and clean_url not in to_visit
                            ):
                                to_visit.append(clean_url)
                except Exception:
                    # For MVP, just skip URLs that fail to load
                    continue

        return [Url(value=url) for url in list(discovered)[:max_pages]]
