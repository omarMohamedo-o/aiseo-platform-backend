"""Application service: register a website for a tenant.

Orchestration only -- no infrastructure construction here. Dependencies are
injected by the composition root.
"""

from __future__ import annotations

from aiseo.domain.value_objects import TenantId, Url
from aiseo.domain.websites.website import Website
from aiseo.ports.persistence.website_repository import WebsiteRepository


class RegisterWebsiteService:
    def __init__(self, website_repository: WebsiteRepository) -> None:
        self._website_repository = website_repository

    async def register(self, tenant_id: TenantId, url: Url) -> Website:
        existing = await self._website_repository.get_by_url(tenant_id, url)
        if existing is not None:
            return existing  # idempotent: registering the same URL twice is a no-op

        website = Website.register(tenant_id=tenant_id, url=url)
        await self._website_repository.add(website)
        return website
