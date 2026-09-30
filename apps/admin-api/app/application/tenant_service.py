"""Application service for managing Tenants (Clients)."""

from __future__ import annotations

import uuid
from typing import Protocol

from apps.admin_api.app.domain.admin_user import AdminUser
from apps.admin_api.app.domain.tenant import SubscriptionTier, Tenant


class TenantRepository(Protocol):
    """Protocol for persisting tenants."""

    async def get(self, tenant_id: uuid.UUID) -> Tenant | None: ...

    async def save(self, tenant: Tenant) -> None: ...


class TenantService:
    """Use cases for managing client accounts."""

    def __init__(self, tenant_repo: TenantRepository) -> None:
        self._tenant_repo = tenant_repo

    async def register_tenant(
        self,
        company_name: str,
        contact_email: str,
        admin: AdminUser,
    ) -> Tenant:
        """Onboard a new client into the platform."""

        # Just requires standard admin access

        tenant = Tenant(
            id=uuid.uuid4(),
            company_name=company_name,
            contact_email=contact_email,
        )

        await self._tenant_repo.save(tenant)
        return tenant

    async def upgrade_tenant(
        self,
        tenant_id: uuid.UUID,
        new_tier: SubscriptionTier,
        admin: AdminUser,
    ) -> Tenant:
        """Upgrade or downgrade a tenant's subscription tier."""

        tenant = await self._tenant_repo.get(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found.")

        updated_tenant = tenant.upgrade_tier(new_tier)
        await self._tenant_repo.save(updated_tenant)
        return updated_tenant
