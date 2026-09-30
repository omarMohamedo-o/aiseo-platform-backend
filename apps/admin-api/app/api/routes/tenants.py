"""FastAPI routes for Tenant management."""

from __future__ import annotations

import uuid

from apps.admin_api.app.api.dependencies import get_current_admin
from apps.admin_api.app.application.tenant_service import TenantService
from apps.admin_api.app.domain.admin_user import AdminUser
from apps.admin_api.app.domain.tenant import SubscriptionTier, Tenant
from apps.admin_api.app.infrastructure.repositories.in_memory_tenant_repo import (
    InMemoryTenantRepository,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/admin/tenants", tags=["Tenants"])

tenant_repo = InMemoryTenantRepository()
tenant_service = TenantService(tenant_repo)


class RegisterTenantRequest(BaseModel):
    company_name: str
    contact_email: str


class UpgradeTenantRequest(BaseModel):
    tier: SubscriptionTier


@router.post("")
async def create_tenant(
    payload: RegisterTenantRequest,
    admin: AdminUser = Depends(get_current_admin),
) -> Tenant:
    """Register a new client/tenant in the platform."""
    return await tenant_service.register_tenant(
        company_name=payload.company_name,
        contact_email=payload.contact_email,
        admin=admin,
    )


@router.put("/{tenant_id}/tier")
async def upgrade_tenant(
    tenant_id: uuid.UUID,
    payload: UpgradeTenantRequest,
    admin: AdminUser = Depends(get_current_admin),
) -> Tenant:
    """Upgrade or downgrade a tenant's subscription tier and quotas."""
    return await tenant_service.upgrade_tenant(
        tenant_id=tenant_id,
        new_tier=payload.tier,
        admin=admin,
    )
