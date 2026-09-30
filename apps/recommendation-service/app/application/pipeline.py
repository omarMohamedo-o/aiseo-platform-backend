"""Recommendation Pipeline orchestrator.

Ties the ChangePlanner and ContentGenerator together.
"""

from __future__ import annotations

from collections.abc import Sequence

from apps.editor_service.app.domain.models import ContentChange
from apps.recommendation_service.app.application.generator import ContentGenerator
from apps.recommendation_service.app.domain.planner import ChangePlanner
from apps.visibility_service.app.seo.domain.scan_snapshot import ScanSnapshot


class RecommendationPipeline:
    """The main entrypoint for the Recommendation Engine.

    1. Reads a ScanSnapshot
    2. Plans fixes using rules
    3. Generates content using AI
    4. Returns a list of SUGGESTED changes
    """

    def __init__(self, planner: ChangePlanner, generator: ContentGenerator) -> None:
        self._planner = planner
        self._generator = generator

    async def process_snapshot(self, snapshot: ScanSnapshot) -> Sequence[ContentChange]:
        """Process a completed scan and return AI-generated recommendations."""

        # 1. Rule-based detection
        fix_requests = self._planner.plan_fixes(snapshot)

        if not fix_requests:
            return []

        # 2. AI-based generation
        changes = await self._generator.generate_fixes(
            website_id=snapshot.website_id,
            tenant_id=snapshot.tenant_id,
            scan_id=snapshot.id,
            requests=fix_requests,
        )

        return changes
