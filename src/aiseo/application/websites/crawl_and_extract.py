"""Application service: orchestrates crawling and extracting a website."""
from __future__ import annotations

import logging

from aiseo.domain.value_objects import TenantId, WebsiteId
from aiseo.domain.websites.page import WebPage
from aiseo.ports.crawler.crawler_port import CrawlerPort
from aiseo.ports.persistence.website_repository import WebsiteRepository
from aiseo.ports.scraper.scraper_port import ScraperPort

logger = logging.getLogger(__name__)


class CrawlAndExtractService:
    def __init__(
        self,
        website_repository: WebsiteRepository,
        crawler_port: CrawlerPort,
        scraper_port: ScraperPort,
    ) -> None:
        self._website_repository = website_repository
        self._crawler = crawler_port
        self._scraper = scraper_port

    async def run(self, tenant_id: TenantId, website_id: WebsiteId) -> None:
        website = await self._website_repository.get(tenant_id, website_id)
        if not website:
            logger.error(f"Website {website_id.value} not found.")
            return

        # Start Crawl
        website = website.start_crawl()
        await self._website_repository.update(website)

        try:
            # 1. Crawl to discover pages
            discovered_urls = await self._crawler.discover_pages(website.url, max_pages=5) # 5 for MVP speed
            website.discovered_urls = discovered_urls
            
            # 2. Extract content for each discovered page
            # (In a real system, this would spawn celery tasks per page)
            for page_url in discovered_urls:
                page = WebPage.discover(website_id=website.id, tenant_id=tenant_id, url=page_url)
                page = page.start_scrape()
                
                try:
                    structured_content = await self._scraper.extract_content(page_url)
                    page = page.complete_scrape(structured_content)
                    # Here we would persist the `page` entity to a PageRepository
                    logger.info(f"Successfully extracted content for {page_url.value}")
                except Exception as e:
                    logger.error(f"Failed to extract content for {page_url.value}: {e}")
                    page = page.fail()

            # Complete Crawl
            website = website.complete_crawl()
            await self._website_repository.update(website)
            
        except Exception:
            logger.exception(f"Crawl and extract failed for {website.url.value}")
            website = website.fail()
            await self._website_repository.update(website)
