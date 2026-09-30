"""Replaceable clustering algorithm port.

Defined as a `Protocol`; concrete algorithms (HDBSCAN, KMeans, ...) compose
the underlying library object privately rather than inheriting from a shared
base class.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class TopicCluster(BaseModel):
    cluster_id: str
    representative_document_indices: list[int]
    centroid: list[float] | None = None
    confidence: float


@runtime_checkable
class ClusteringAlgorithm(Protocol):
    def cluster(self, vectors: list[list[float]]) -> list[TopicCluster]: ...
