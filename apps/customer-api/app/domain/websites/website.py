"""Website aggregate root."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from aiseo.domain.value_objects import TenantId, Url, WebsiteId


class WebsiteStatus(str, Enum):
    REGISTERED = "REGISTERED"
    CRAWLING = "CRAWLING"
    CRAWLED = "CRAWLED"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    FAILED = "FAILED"


class Website(BaseModel):
    """Aggregate root. Owns its own status transitions; nothing external
    mutates `status` directly (no `set_status`)."""

    model_config = ConfigDict(extra="forbid")

    id: WebsiteId
    tenant_id: TenantId
    url: Url
    discovered_urls: list[Url] = []
    status: WebsiteStatus = WebsiteStatus.REGISTERED
    created_at: datetime
    updated_at: datetime

    @classmethod
    def register(cls, tenant_id: TenantId, url: Url) -> Website:
        now = datetime.now(UTC)
        return cls(
            id=WebsiteId(value=uuid.uuid4()),
            tenant_id=tenant_id,
            url=url,
            status=WebsiteStatus.REGISTERED,
            created_at=now,
            updated_at=now,
        )

    def start_crawl(self) -> Website:
        return self.model_copy(
            update={"status": WebsiteStatus.CRAWLING, "updated_at": datetime.now(UTC)}
        )

    def complete_crawl(self) -> Website:
        return self.model_copy(
            update={"status": WebsiteStatus.CRAWLED, "updated_at": datetime.now(UTC)}
        )

    def fail(self) -> Website:
        return self.model_copy(
            update={"status": WebsiteStatus.FAILED, "updated_at": datetime.now(UTC)}
        )
