"""Repository port. SQLAlchemy models never leak past the adapter boundary.

Defined as a `Protocol`; the in-memory and (future) SQLAlchemy adapters
implement it structurally, holding their storage (dict, session, ...) as a
private attribute rather than inheriting from this class.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from aiseo.domain.value_objects import TenantId, Url, WebsiteId
from aiseo.domain.websites.website import Website


@runtime_checkable
class WebsiteRepository(Protocol):
    async def add(self, website: Website) -> None: ...

    async def get(self, tenant_id: TenantId, website_id: WebsiteId) -> Website | None: ...

    async def get_by_url(self, tenant_id: TenantId, url: Url) -> Website | None: ...

    async def list_for_tenant(self, tenant_id: TenantId) -> list[Website]: ...

    async def update(self, website: Website) -> None: ...
