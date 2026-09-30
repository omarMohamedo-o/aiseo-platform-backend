"""In-memory repository for Tenants."""

from __future__ import annotations

import uuid

from apps.admin_api.app.domain.tenant import Tenant


class InMemoryTenantRepository:
    """Mock repository for storing tenants."""

    def __init__(self) -> None:
        self._tenants: dict[uuid.UUID, Tenant] = {}

    async def get(self, tenant_id: uuid.UUID) -> Tenant | None:
        return self._tenants.get(tenant_id)

    async def save(self, tenant: Tenant) -> None:
        self._tenants[tenant.id] = tenant
