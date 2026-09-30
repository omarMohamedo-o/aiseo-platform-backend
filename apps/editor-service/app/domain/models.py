"""Domain models for the website auto-edit system.

These models represent content changes that the platform recommends and
can automatically apply to client websites through CMS APIs, Edge Workers,
or JS Snippet injection.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ChangeType(str, Enum):
    """Type of SEO change to apply."""

    META_TITLE = "meta_title"
    META_DESCRIPTION = "meta_description"
    HEADING_H1 = "heading_h1"
    HEADING_HIERARCHY = "heading_hierarchy"
    IMAGE_ALT_TEXT = "image_alt_text"
    STRUCTURED_DATA = "structured_data"
    CANONICAL_TAG = "canonical_tag"
    OPEN_GRAPH = "open_graph"
    FAQ_SECTION = "faq_section"
    INTERNAL_LINK = "internal_link"
    CONTENT_SECTION = "content_section"
    ROBOTS_TXT = "robots_txt"
    SITEMAP = "sitemap"


class ChangeStatus(str, Enum):
    """Lifecycle status of a content change."""

    SUGGESTED = "SUGGESTED"  # AI generated, waiting for review
    PENDING = "PENDING"  # Approved by client, waiting to apply
    APPLYING = "APPLYING"  # Currently being applied
    APPLIED = "APPLIED"  # Successfully applied to website
    VERIFIED = "VERIFIED"  # Follow-up scan confirmed the change
    FAILED = "FAILED"  # Failed to apply
    ROLLED_BACK = "ROLLED_BACK"  # Change was reverted
    REJECTED = "REJECTED"  # Client rejected the suggestion


class ChangePriority(str, Enum):
    """Impact priority of the change."""

    CRITICAL = "CRITICAL"  # Missing title, broken structured data
    HIGH = "HIGH"  # Missing meta description, no H1
    MEDIUM = "MEDIUM"  # Image alt text, Open Graph
    LOW = "LOW"  # Minor content improvements


class IntegrationMethod(str, Enum):
    """How the client's website is connected to our platform."""

    CMS_WORDPRESS = "cms_wordpress"
    CMS_SHOPIFY = "cms_shopify"
    CMS_WEBFLOW = "cms_webflow"
    CMS_CUSTOM = "cms_custom"
    EDGE_PROXY = "edge_proxy"
    JS_SNIPPET = "js_snippet"
    MANUAL = "manual"  # Just recommendations, no auto-apply


class WebsiteConnection(BaseModel):
    """Represents how a client's website is connected to our platform.

    Stores the credentials and configuration needed to apply changes.
    """

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    website_id: uuid.UUID
    tenant_id: uuid.UUID
    method: IntegrationMethod
    credentials: dict[str, str] = {}  # Encrypted API keys, tokens, etc.
    base_url: str
    is_active: bool = True
    last_tested_at: datetime | None = None
    created_at: datetime


class ContentChange(BaseModel):
    """A single recommended/applied change to a client's website.

    This is the core unit of the auto-edit system. It tracks the
    full lifecycle from suggestion → approval → application → verification.
    """

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    website_id: uuid.UUID
    tenant_id: uuid.UUID
    scan_id: uuid.UUID  # Which scan triggered this recommendation

    # What to change
    page_url: str
    change_type: ChangeType
    priority: ChangePriority

    # Change details
    description: str  # Human-readable explanation
    before_value: str | None = None  # Current content on the website
    after_value: str  # Proposed new content
    ai_reasoning: str | None = None  # Why the AI suggested this

    # Lifecycle
    status: ChangeStatus = ChangeStatus.SUGGESTED
    approved_by: str | None = None  # User who approved
    applied_via: IntegrationMethod | None = None

    # Timestamps
    suggested_at: datetime
    approved_at: datetime | None = None
    applied_at: datetime | None = None
    verified_at: datetime | None = None
    rolled_back_at: datetime | None = None

    # Error tracking
    error_message: str | None = None
    retry_count: int = 0

    @classmethod
    def suggest(
        cls,
        website_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scan_id: uuid.UUID,
        page_url: str,
        change_type: ChangeType,
        priority: ChangePriority,
        description: str,
        before_value: str | None,
        after_value: str,
        ai_reasoning: str | None = None,
    ) -> ContentChange:
        return cls(
            id=uuid.uuid4(),
            website_id=website_id,
            tenant_id=tenant_id,
            scan_id=scan_id,
            page_url=page_url,
            change_type=change_type,
            priority=priority,
            description=description,
            before_value=before_value,
            after_value=after_value,
            ai_reasoning=ai_reasoning,
            status=ChangeStatus.SUGGESTED,
            suggested_at=datetime.now(UTC),
        )

    def approve(self, approved_by: str) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.PENDING,
                "approved_by": approved_by,
                "approved_at": datetime.now(UTC),
            }
        )

    def reject(self) -> ContentChange:
        return self.model_copy(update={"status": ChangeStatus.REJECTED})

    def start_applying(self, method: IntegrationMethod) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.APPLYING,
                "applied_via": method,
            }
        )

    def mark_applied(self) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.APPLIED,
                "applied_at": datetime.now(UTC),
            }
        )

    def mark_verified(self) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.VERIFIED,
                "verified_at": datetime.now(UTC),
            }
        )

    def mark_failed(self, error: str) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.FAILED,
                "error_message": error,
                "retry_count": self.retry_count + 1,
            }
        )

    def rollback(self) -> ContentChange:
        return self.model_copy(
            update={
                "status": ChangeStatus.ROLLED_BACK,
                "rolled_back_at": datetime.now(UTC),
            }
        )


class ChangeResult(BaseModel):
    """Result of attempting to apply a content change."""

    model_config = ConfigDict(extra="forbid")

    success: bool
    change_id: uuid.UUID
    message: str
    applied_via: IntegrationMethod
    verified: bool = False
    error: str | None = None
