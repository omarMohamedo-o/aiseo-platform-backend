"""Admin User domain models and Role-Based Access Control (RBAC)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AdminRole(str, Enum):
    """Roles for internal platform administrators."""

    SUPERADMIN = "SUPERADMIN"  # Can change global configs, AI models, billing
    SUPPORT = "SUPPORT"  # Can view tenants and run diagnostics, but no config changes


class AdminUser(BaseModel):
    """An internal employee/system administrator."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    email: str
    role: AdminRole
    is_active: bool = True
    last_login_at: datetime | None = None
    created_at: datetime = datetime.now(UTC)

    def can_manage_config(self) -> bool:
        """Only superadmins can change global routing and scoring weights."""
        return self.role == AdminRole.SUPERADMIN
