"""Production Prometheus & OpenMetrics Telemetry Exporter.

Exposes real-time AISEO/GEO audit metrics, cache performance, and latency counters
for Prometheus scraping and Grafana dashboards.

Zero third-party daemon dependency; strictly compliant with OpenMetrics exposition spec.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import threading
import time
from typing import ClassVar


class MetricsRegistry:
    """Thread-safe Prometheus / OpenMetrics metric registry."""

    _instance: ClassVar[MetricsRegistry | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self) -> None:
        self._mutex = threading.Lock()
        self._counters: dict[str, dict[tuple[tuple[str, str], ...], float]] = {
            "aiseo_audits_total": {},
            "aiseo_cache_hits_total": {},
            "aiseo_cache_misses_total": {},
        }
        self._gauges: dict[str, dict[tuple[tuple[str, str], ...], float]] = {
            "aiseo_geo_visibility_score": {},
            "aiseo_hallucination_score": {},
            "aiseo_pipeline_latency_seconds": {},
        }

    @classmethod
    def get_instance(cls) -> MetricsRegistry:
        """Singleton accessor for application metrics."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _labels_to_key(self, labels: dict[str, str]) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(labels.items()))

    def _format_labels(self, key: tuple[tuple[str, str], ...]) -> str:
        if not key:
            return ""
        items = [f'{k}="{v}"' for k, v in key]
        return "{" + ",".join(items) + "}"

    def record_audit(self, brand: str, status: str = "success") -> None:
        """Increments audit execution counter."""
        key = self._labels_to_key({"brand": brand, "status": status})
        with self._mutex:
            current = self._counters["aiseo_audits_total"].get(key, 0.0)
            self._counters["aiseo_audits_total"][key] = current + 1.0

    def record_cache_hit(self, tier: str = "l1") -> None:
        """Increments semantic cache hit counter."""
        key = self._labels_to_key({"tier": tier})
        with self._mutex:
            current = self._counters["aiseo_cache_hits_total"].get(key, 0.0)
            self._counters["aiseo_cache_hits_total"][key] = current + 1.0

    def record_cache_miss(self, tier: str = "l1") -> None:
        """Increments semantic cache miss counter."""
        key = self._labels_to_key({"tier": tier})
        with self._mutex:
            current = self._counters["aiseo_cache_misses_total"].get(key, 0.0)
            self._counters["aiseo_cache_misses_total"][key] = current + 1.0

    def set_visibility(self, brand: str, score: float) -> None:
        """Sets current GEO Visibility gauge (0-100)."""
        key = self._labels_to_key({"brand": brand})
        with self._mutex:
            self._gauges["aiseo_geo_visibility_score"][key] = float(score)

    def set_hallucination(self, brand: str, score: float) -> None:
        """Sets current RAG hallucination score gauge (0.0-1.0)."""
        key = self._labels_to_key({"brand": brand})
        with self._mutex:
            self._gauges["aiseo_hallucination_score"][key] = float(score)

    def record_latency(self, stage: str, seconds: float) -> None:
        """Records pipeline stage execution latency in seconds."""
        key = self._labels_to_key({"stage": stage})
        with self._mutex:
            self._gauges["aiseo_pipeline_latency_seconds"][key] = float(seconds)

    def export_prometheus_text(self) -> str:
        """Renders OpenMetrics / Prometheus exposition text format."""
        lines: list[str] = [
            "# AISEO & GEO Enterprise Telemetry Exporter",
            "# Author: Omar Mohamed (@omarMohamedo-o)",
            "",
        ]

        # Descriptions & Help
        docstrings = {
            "aiseo_audits_total": ("Total number of brand visibility audits executed", "counter"),
            "aiseo_cache_hits_total": ("Total semantic cache hits across tiers", "counter"),
            "aiseo_cache_misses_total": ("Total semantic cache misses across tiers", "counter"),
            "aiseo_geo_visibility_score": ("Current GEO visibility index score (0-100)", "gauge"),
            "aiseo_hallucination_score": ("Current RAG hallucination ratio (0.0-1.0)", "gauge"),
            "aiseo_pipeline_latency_seconds": ("Pipeline execution duration in seconds", "gauge"),
        }

        with self._mutex:
            for name, (help_text, metric_type) in docstrings.items():
                lines.append(f"# HELP {name} {help_text}")
                lines.append(f"# TYPE {name} {metric_type}")
                
                samples = self._counters.get(name) or self._gauges.get(name) or {}
                if not samples:
                    lines.append(f"{name} 0.0")
                else:
                    for key, val in sorted(samples.items()):
                        lbls = self._format_labels(key)
                        lines.append(f"{name}{lbls} {val}")
                lines.append("")

        return "\n".join(lines)


# Global singleton exporter instance
metrics_registry = MetricsRegistry.get_instance()

