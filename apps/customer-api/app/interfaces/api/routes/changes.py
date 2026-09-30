"""Customer API routes for managing and approving auto-edits."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/websites/{website_id}/changes", tags=["Auto-Edits"])


class ApproveChangeRequest(BaseModel):
    approved_by_user_id: str


@router.get("")
async def list_pending_changes(website_id: uuid.UUID) -> list[dict[str, Any]]:
    """List all AI-suggested changes that are waiting for client approval."""
    # Mocked list of pending changes
    return [
        {
            "change_id": str(uuid.uuid4()),
            "type": "META_DESCRIPTION",
            "page_url": "https://example.com/about",
            "priority": "HIGH",
            "description": "Missing meta description",
            "proposed_fix": "Learn more about Example Corp, the leading provider of enterprise CRM software...",
            "status": "SUGGESTED",
        }
    ]


@router.post("/{change_id}/approve")
async def approve_change(
    website_id: uuid.UUID, change_id: uuid.UUID, payload: ApproveChangeRequest
) -> dict[str, Any]:
    """Approve a suggested change and trigger the Editor Service to apply it."""
    # In reality, this updates the status to PENDING and triggers the EditorService
    return {
        "change_id": str(change_id),
        "status": "APPLYING",
        "message": "Change approved. Applying to website via CMS integration.",
    }
