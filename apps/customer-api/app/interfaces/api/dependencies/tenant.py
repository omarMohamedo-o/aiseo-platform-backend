"""Resolves the current tenant from the request. Real auth/RBAC (Phase 2)
replaces this header-based placeholder without touching business logic."""

from __future__ import annotations

import uuid

from fastapi import Header, HTTPException

from aiseo.domain.value_objects import TenantId


def get_current_tenant(x_tenant_id: str = Header(...)) -> TenantId:
    try:
        return TenantId(value=uuid.UUID(x_tenant_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid X-Tenant-Id header") from exc
