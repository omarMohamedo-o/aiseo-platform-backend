"""In-memory adapter satisfying the `WebsiteRepository` protocol via
composition (a private dict), not inheritance. A PostgreSQL/SQLAlchemy
adapter can be added later without touching application/domain code."""

from __future__ import annotations

from aiseo.domain.value_objects import TenantId, Url, WebsiteId
from aiseo.domain.websites.website import Website
from aiseo.infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class InMemoryWebsiteRepository:
    def __init__(self) -> None:
        self.__store: dict[tuple[str, str], Website] = {}

    async def add(self, website: Website) -> None:
        key = (str(website.tenant_id.value), str(website.id.value))
        self.__store[key] = website
        logger.debug("website_repository.add", website_id=str(website.id.value))

    async def get(self, tenant_id: TenantId, website_id: WebsiteId) -> Website | None:
        return self.__store.get((str(tenant_id.value), str(website_id.value)))

    async def get_by_url(self, tenant_id: TenantId, url: Url) -> Website | None:
        for website in self.__store.values():
            if (
                str(website.tenant_id.value) == str(tenant_id.value)
                and website.url.value == url.value
            ):
                return website
        return None

    async def list_for_tenant(self, tenant_id: TenantId) -> list[Website]:
        return [w for w in self.__store.values() if str(w.tenant_id.value) == str(tenant_id.value)]
