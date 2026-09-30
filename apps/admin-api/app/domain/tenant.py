"""Tenant (Client) domain models for the Admin API."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class SubscriptionTier(str, Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"


class TenantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


class Tenant(BaseModel):
    """A client/company using the platform."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    company_name: str
    contact_email: str

    tier: SubscriptionTier = SubscriptionTier.FREE
    status: TenantStatus = TenantStatus.ACTIVE

    # Quotas
    monthly_scan_quota: int = 10
    scans_used_this_month: int = 0

    created_at: datetime = datetime.now(UTC)

    def suspend(self) -> Tenant:
        return self.model_copy(update={"status": TenantStatus.SUSPENDED})

    def activate(self) -> Tenant:
        return self.model_copy(update={"status": TenantStatus.ACTIVE})

    def upgrade_tier(self, new_tier: SubscriptionTier) -> Tenant:
        # Simple quota logic based on tier
        quota = 10
        if new_tier == SubscriptionTier.PRO:
            quota = 100
        elif new_tier == SubscriptionTier.ENTERPRISE:
            quota = 10000

        return self.model_copy(
            update={
                "tier": new_tier,
                "monthly_scan_quota": quota,
            }
        )
