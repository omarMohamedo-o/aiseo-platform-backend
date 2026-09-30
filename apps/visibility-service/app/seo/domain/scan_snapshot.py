"""Domain model for a timestamped scan snapshot.

Each scan produces a snapshot that captures all SEO/AEO/GEO metrics at
a specific point in time. Snapshots enable before/after comparison and
historical trend tracking.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from apps.visibility_service.app.seo.domain.page_seo_audit import PageSeoAudit
from apps.visibility_service.app.seo.domain.serp_result import SerpResult
from apps.visibility_service.app.seo.domain.technical_seo import TechnicalSeoAudit
from pydantic import BaseModel, ConfigDict


class ScanStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ScoreBreakdown(BaseModel):
    """Detailed score breakdown for display."""

    model_config = ConfigDict(extra="forbid")

    overall: float  # 0-100
    technical: float | None = None
    on_page: float | None = None
    content: float | None = None
    rankings: float | None = None


class AppliedChange(BaseModel):
    """A record of a change that was auto-applied during/after this scan."""

    model_config = ConfigDict(extra="forbid")

    page_url: str
    change_type: str  # "meta_description", "structured_data", "heading_fix", etc.
    description: str
    before_value: str | None = None
    after_value: str | None = None
    applied_at: datetime


class ScanSnapshot(BaseModel):
    """A complete point-in-time snapshot of all visibility metrics.

    This is the core data structure for before/after comparison and
    historical trend tracking. Every scan produces one of these.
    """

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    website_id: uuid.UUID
    tenant_id: uuid.UUID

    scan_number: int
    status: ScanStatus = ScanStatus.PENDING

    # Scores
    seo_score: ScoreBreakdown | None = None
    aeo_score: ScoreBreakdown | None = None
    geo_score: ScoreBreakdown | None = None

    # Detailed audit data
    technical_audit: TechnicalSeoAudit | None = None
    page_audits: list[PageSeoAudit] = []
    serp_results: list[SerpResult] = []

    # Changes applied
    applied_changes: list[AppliedChange] = []

    # Metadata
    pages_crawled: int = 0
    pages_analyzed: int = 0
    keywords_tracked: int = 0

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime

    @classmethod
    def create(
        cls,
        website_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scan_number: int,
    ) -> ScanSnapshot:
        return cls(
            id=uuid.uuid4(),
            website_id=website_id,
            tenant_id=tenant_id,
            scan_number=scan_number,
            status=ScanStatus.PENDING,
            created_at=datetime.now(UTC),
        )

    def start(self) -> ScanSnapshot:
        return self.model_copy(
            update={
                "status": ScanStatus.RUNNING,
                "started_at": datetime.now(UTC),
            }
        )

    def complete(
        self,
        seo_score: ScoreBreakdown,
        technical_audit: TechnicalSeoAudit,
        page_audits: list[PageSeoAudit],
        serp_results: list[SerpResult],
    ) -> ScanSnapshot:
        return self.model_copy(
            update={
                "status": ScanStatus.COMPLETED,
                "seo_score": seo_score,
                "technical_audit": technical_audit,
                "page_audits": page_audits,
                "serp_results": serp_results,
                "pages_analyzed": len(page_audits),
                "keywords_tracked": len(serp_results),
                "completed_at": datetime.now(UTC),
            }
        )

    def fail(self) -> ScanSnapshot:
        return self.model_copy(
            update={
                "status": ScanStatus.FAILED,
                "completed_at": datetime.now(UTC),
            }
        )
