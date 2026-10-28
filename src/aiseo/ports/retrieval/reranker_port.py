"""Abstract port interface for Hybrid Search and Cross-Encoder Reranking."""
from __future__ import annotations

from abc import ABC, abstractmethod

from aiseo.domain.evaluation.rerank import RerankCandidate, SnippetPrediction


class RerankerPort(ABC):
    """Port interface for semantic reranking and AEO snippet prediction."""

    @abstractmethod
    async def rerank(
        self,
        query: str,
        candidates: list[RerankCandidate],
        top_k: int = 5,
    ) -> list[RerankCandidate]:
        """Rank passage candidates using hybrid fusion (BM25 + Dense) and cross-encoder scoring."""
        raise NotImplementedError

    @abstractmethod
    async def predict_aeo_snippet(
        self,
        question: str,
        passages: list[str],
        brand: str | None = None,
    ) -> SnippetPrediction:
        """Predict the optimal 40-60 word snippet likely to be extracted as a Google Featured Snippet or Perplexity answer."""
        raise NotImplementedError

