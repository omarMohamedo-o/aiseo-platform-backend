"""Stable, versioned API DTOs. Domain entities are never returned directly."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from aiseo.domain.websites.website import Website, WebsiteStatus


class RegisterWebsiteRequest(BaseModel):
    url: str = Field(
        ..., description="Absolute URL of the site to register, e.g. https://example.com"
    )


class WebsiteResponse(BaseModel):
    id: uuid.UUID
    url: str
    status: WebsiteStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, website: Website) -> WebsiteResponse:
        return cls(
            id=website.id.value,
            url=website.url.value,
            status=website.status,
            created_at=website.created_at,
            updated_at=website.updated_at,
        )
