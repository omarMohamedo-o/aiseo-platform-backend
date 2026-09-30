"""Domain models for a crawled and scraped web page."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from aiseo.domain.analysis.entities import Entity, Keyword
from aiseo.domain.value_objects import TenantId, Url, WebsiteId


class PageId(BaseModel):
    value: uuid.UUID


class PageStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    SCRAPING = "SCRAPING"
    SCRAPED = "SCRAPED"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    FAILED = "FAILED"


class ContentSection(BaseModel):
    """A semantic section extracted from a web page."""

    heading: str | None
    content: str


class StructuredContent(BaseModel):
    """The structured representation of a page's content."""

    title: str | None
    language: str | None
    sections: list[ContentSection]
    raw_text: str  # The full clean text for embeddings/LLMs


class WebPage(BaseModel):
    """Domain entity representing a specific page on a website."""

    model_config = ConfigDict(extra="forbid")

    id: PageId
    website_id: WebsiteId
    tenant_id: TenantId
    url: Url
    status: PageStatus = PageStatus.DISCOVERED
    structured_content: StructuredContent | None = None
    entities: list[Entity] = []
    keywords: list[Keyword] = []
    created_at: datetime
    updated_at: datetime

    @classmethod
    def discover(cls, website_id: WebsiteId, tenant_id: TenantId, url: Url) -> WebPage:
        now = datetime.now(UTC)
        return cls(
            id=PageId(value=uuid.uuid4()),
            website_id=website_id,
            tenant_id=tenant_id,
            url=url,
            status=PageStatus.DISCOVERED,
            created_at=now,
            updated_at=now,
        )

    def start_scrape(self) -> WebPage:
        return self.model_copy(
            update={"status": PageStatus.SCRAPING, "updated_at": datetime.now(UTC)}
        )

    def complete_scrape(self, content: StructuredContent) -> WebPage:
        return self.model_copy(
            update={
                "status": PageStatus.SCRAPED,
                "structured_content": content,
                "updated_at": datetime.now(UTC),
            }
        )

    def start_analysis(self) -> WebPage:
        return self.model_copy(
            update={"status": PageStatus.ANALYZING, "updated_at": datetime.now(UTC)}
        )

    def complete_analysis(self, entities: list[Entity], keywords: list[Keyword]) -> WebPage:
        return self.model_copy(
            update={
                "status": PageStatus.ANALYZED,
                "entities": entities,
                "keywords": keywords,
                "updated_at": datetime.now(UTC),
            }
        )

    def fail(self) -> WebPage:
        return self.model_copy(
            update={"status": PageStatus.FAILED, "updated_at": datetime.now(UTC)}
        )
