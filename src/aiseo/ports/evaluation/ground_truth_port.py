"""Abstract port for empirical Ground Truth verification using free and open-source data."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from aiseo.domain.evaluation.ground_truth import GroundTruthValidationResult


@runtime_checkable
class GroundTruthPort(Protocol):
    """Verifies GEO/AEO audit scores against real-world search engines and knowledge graphs."""

    async def verify_domain(
        self,
        domain: str,
        brand: str,
        keywords: list[str] | None = None,
    ) -> GroundTruthValidationResult:
        """Query free Google Suggest, Wikidata, and DuckDuckGo endpoints to validate real authority."""
        ...

