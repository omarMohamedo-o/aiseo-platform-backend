"""Customer API routes for triggering and viewing scans."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter

# In a full app, these would be injected via Dependencies
# For MVP, we mock the dependency injection
router = APIRouter(prefix="/websites/{website_id}/scans", tags=["Scans"])


@router.post("")
async def trigger_scan(website_id: uuid.UUID) -> dict[str, Any]:
    """Trigger a new SEO/AEO/GEO scan for a registered website.

    In a real system, this would queue a background task. For the MVP,
    we return a mocked task acknowledgment.
    """
    return {
        "scan_id": str(uuid.uuid4()),
        "status": "QUEUED",
        "message": "Scan triggered successfully and sent to crawler-service.",
    }


@router.get("/latest")
async def get_latest_scan_results(website_id: uuid.UUID) -> dict[str, Any]:
    """Fetch the dashboard data for the most recent scan."""
    # Mocked Dashboard Data for the Customer UI
    return {
        "website_id": str(website_id),
        "scores": {
            "seo": 74,
            "aeo": 68,
            "geo": 63,
        },
        "technical": {
            "page_speed_mobile": 85,
            "has_sitemap": True,
            "has_ssl": True,
        },
        "recent_rankings": [
            {"query": "best startup crm", "position": 7, "change": "+11"},
            {"query": "crm pricing", "position": 12, "change": "+13"},
        ],
    }
