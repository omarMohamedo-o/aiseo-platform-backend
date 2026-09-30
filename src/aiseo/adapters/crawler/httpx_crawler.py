"""httpx-based crawler adapter."""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

import httpx
import structlog
from bs4 import BeautifulSoup

from aiseo.domain.value_objects import Url
from aiseo.ports.crawler.crawler_port import CrawlerPort

logger = structlog.get_logger(__name__)


class HttpxCrawler(CrawlerPort):
    def __init__(self, timeout: float = 12.0) -> None:
        self._timeout = timeout
        self.last_total_detected: int = 0

    async def _fetch_sitemap_urls(self, client: httpx.AsyncClient, origin: str, base_domain: str) -> set[str]:
        """Discover pages via sitemap.xml, sitemap_index.xml, and robots.txt."""
        core_domain = base_domain.replace("www.", "")
        sitemap_candidates = [
            f"{origin}/sitemap.xml",
            f"{origin}/sitemap_index.xml",
            f"https://{core_domain}/sitemap.xml",
            f"https://{core_domain}/sitemap_index.xml",
        ]

        # Check robots.txt for custom Sitemap directives
        for rob_origin in [origin, f"https://{core_domain}"]:
            try:
                robots_resp = await client.get(f"{rob_origin}/robots.txt")
                if robots_resp.status_code == 200:
                    sitemap_directives = re.findall(r"(?i)^sitemap:\s*(https?://[^\s]+)", robots_resp.text, re.MULTILINE)
                    for s in sitemap_directives:
                        if s not in sitemap_candidates:
                            sitemap_candidates.append(s)
            except Exception as exc:
                logger.debug("Failed to read robots.txt for sitemaps", error=str(exc))

        found_urls: set[str] = set()

        for sitemap_url in sitemap_candidates:
            try:
                resp = await client.get(sitemap_url)
                if resp.status_code == 200 and resp.text:
                    # Check for child sitemaps in index
                    sub_sitemaps = re.findall(r"<sitemap>\s*<loc>(https?://[^<]+)</loc>", resp.text, re.IGNORECASE)
                    for sub in sub_sitemaps[:5]:
                        try:
                            sub_resp = await client.get(sub)
                            if sub_resp.status_code == 200:
                                for loc in re.findall(r"<loc>(https?://[^<]+)</loc>", sub_resp.text, re.IGNORECASE):
                                    loc_clean = loc.strip()
                                    if urlparse(loc_clean).netloc.replace("www.", "") == core_domain:
                                        found_urls.add(loc_clean)
                        except Exception:
                            continue

                    # Direct URLs in this sitemap
                    for loc in re.findall(r"<loc>(https?://[^<]+)</loc>", resp.text, re.IGNORECASE):
                        loc_clean = loc.strip()
                        if urlparse(loc_clean).netloc.replace("www.", "") == core_domain:
                            found_urls.add(loc_clean)
            except Exception as exc:
                logger.debug("Failed to fetch sitemap", sitemap=sitemap_url, error=str(exc))

        return found_urls

    async def discover_pages(self, start_url: Url, max_pages: int = 0) -> list[Url]:
        """Discover all internal pages on the website.
        
        If max_pages <= 0, auto-detects and discovers ALL available pages across the site
        (using sitemaps + link graphs, capped by a safety limit of 100 pages).
        """
        safety_cap = 100 if (max_pages <= 0 or max_pages > 100) else max_pages
        effective_limit = safety_cap if max_pages <= 0 else max_pages

        discovered: set[str] = set()
        to_visit: list[str] = [start_url.value]

        parsed_start = urlparse(start_url.value)
        base_domain = parsed_start.netloc
        core_domain = base_domain.replace("www.", "")
        origin = f"{parsed_start.scheme or 'https'}://{base_domain}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AISEO-Crawler/2.0 (compatible; Enterprise Audit Engine)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True, headers=headers) as client:
            # 1. Sitemap-based auto-discovery
            sitemap_urls = await self._fetch_sitemap_urls(client, origin, base_domain)
            for s_url in sitemap_urls:
                if s_url not in to_visit:
                    to_visit.append(s_url)

            self.last_total_detected = max(len(to_visit), len(sitemap_urls), 1)

            # 2. HTML Link Graph traversal
            while to_visit and len(discovered) < effective_limit:
                current_url = to_visit.pop(0)
                if current_url in discovered:
                    continue

                try:
                    response = await client.get(current_url)
                    if response.status_code >= 400:
                        continue

                    discovered.add(current_url)

                    content_type = response.headers.get("content-type", "")
                    if "text/html" in content_type:
                        soup = BeautifulSoup(response.content, "html.parser")
                        for a_tag in soup.find_all("a", href=True):
                            href = str(a_tag["href"]).strip()
                            if href.startswith(("#", "mailto:", "javascript:", "tel:")):
                                continue

                            absolute_url = urljoin(current_url, href)
                            parsed = urlparse(absolute_url)

                            # Stay within the same domain, strip query params and fragments
                            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
                            if not clean_url:
                                continue

                            # Normalize root
                            if clean_url == f"{parsed.scheme}://{parsed.netloc}":
                                clean_url = f"{clean_url}/"

                            if (
                                parsed.netloc.replace("www.", "") == core_domain
                                and clean_url not in discovered
                                and clean_url not in to_visit
                            ):
                                to_visit.append(clean_url)
                except Exception as exc:
                    logger.debug("Failed to crawl url", url=current_url, error=str(exc))
                    continue

        # Helper to get canonical URL key
        def canonicalize(u_str: str) -> str:
            p = urlparse(u_str)
            c_domain = p.netloc.replace("www.", "")
            c_path = p.path.rstrip("/")
            if not c_path:
                c_path = "/"
            return f"{p.scheme or 'https'}://{c_domain}{c_path}"

        seen_canonical: set[str] = set()
        clean_url_list: list[Url] = []

        # Keep start_url at index 0
        canonical_start = canonicalize(start_url.value)
        seen_canonical.add(canonical_start)
        clean_url_list.append(start_url)

        for u_str in list(discovered):
            c = canonicalize(u_str)
            if c not in seen_canonical:
                seen_canonical.add(c)
                clean_url_list.append(Url(value=u_str))

        self.last_total_detected = max(self.last_total_detected, len(seen_canonical) + len(to_visit))

        return clean_url_list[:effective_limit]

