"""Abstract port interface for RAG citation grounding and hallucination detection."""
from __future__ import annotations

from abc import ABC, abstractmethod

from aiseo.domain.evaluation.grounding import HallucinationMetrics


class GroundingGuardPort(ABC):
    """Port for verifying factual grounding of AI responses against source website context."""

    @abstractmethod
    def verify_grounding(
        self,
        answer: str,
        source_context: str | list[str],
        brand: str,
        threshold: float = 0.45,
    ) -> HallucinationMetrics:
        """Evaluate whether factual claims in the answer are grounded in crawled source context.

        Returns HallucinationMetrics containing grounding_ratio (0-1), hallucination_score (0-1),
        and lists of verified vs unverified claims.
        """
        raise NotImplementedError

    @abstractmethod
    def extract_claims(self, text: str) -> list[str]:
        """Extract high-entropy factual claims (pricing, features, metrics, compliance certifications)."""
        raise NotImplementedError
