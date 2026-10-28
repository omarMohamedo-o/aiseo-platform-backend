"""Unit tests for Prometheus Telemetry Exporter.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aiseo.api.app import create_app
from aiseo.infrastructure.monitoring.metrics import MetricsRegistry
from tests.test_config import TARGET_BRAND


def test_metrics_registry_records_and_exports() -> None:
    reg = MetricsRegistry()
    reg.record_audit(brand=TARGET_BRAND, status="success")
    reg.record_cache_hit(tier="l1")
    reg.record_cache_miss(tier="l2")
    reg.set_visibility(brand=TARGET_BRAND, score=88.5)
    reg.set_hallucination(brand=TARGET_BRAND, score=0.08)
    reg.record_latency(stage="rerank", seconds=0.042)

    output = reg.export_prometheus_text()
    assert "# HELP aiseo_audits_total" in output
    assert "# TYPE aiseo_audits_total counter" in output
    assert f'aiseo_audits_total{{brand="{TARGET_BRAND}",status="success"}} 1.0' in output
    assert 'aiseo_cache_hits_total{tier="l1"} 1.0' in output
    assert 'aiseo_cache_misses_total{tier="l2"} 1.0' in output
    assert f'aiseo_geo_visibility_score{{brand="{TARGET_BRAND}"}} 88.5' in output
    assert f'aiseo_hallucination_score{{brand="{TARGET_BRAND}"}} 0.08' in output
    assert 'aiseo_pipeline_latency_seconds{stage="rerank"} 0.042' in output


def test_metrics_http_endpoint() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "# AISEO & GEO Enterprise Telemetry Exporter" in response.text
    assert "aiseo_audits_total" in response.text

