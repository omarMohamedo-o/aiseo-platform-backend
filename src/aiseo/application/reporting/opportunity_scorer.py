"""Application service for calculating keyword opportunity scores and monitoring shift alerts."""
from __future__ import annotations

import re
import uuid
from typing import Any

from aiseo.domain.reporting.report_models import OpportunityAlert, OpportunityScore, ReportKeyword
from aiseo.infrastructure.configuration.modules.opportunity_config import OpportunityScorerConfig


def calculate_opportunity_score(
    keyword_row: ReportKeyword | dict[str, Any],
    config: OpportunityScorerConfig | None = None,
) -> int:
    """Calculate an Opportunity Score (0-100) based on configuration-driven weights and benchmarks."""
    cfg = config or OpportunityScorerConfig()

    if isinstance(keyword_row, dict):
        raw_vol = str(keyword_row.get("volume", "0"))
        raw_diff = keyword_row.get("difficulty", 0)
        raw_cpc = str(keyword_row.get("cpc", "0"))
        raw_serp = keyword_row.get("serp_features", keyword_row.get("serpFeatures", 0))
    else:
        raw_vol = keyword_row.volume
        raw_diff = keyword_row.difficulty
        raw_cpc = keyword_row.cpc
        raw_serp = keyword_row.serp_features

    # Parse volume
    vol_clean = re.sub(r"[^\d.]", "", raw_vol) or "0"
    volume_num = float(vol_clean)
    volume_normalized = min(100.0, (volume_num / cfg.max_volume_normalization) * 100.0)

    # Parse difficulty
    try:
        difficulty_num = float(raw_diff) if raw_diff is not None else 0.0
    except (ValueError, TypeError):
        difficulty_num = 0.0

    # Parse CPC
    cpc_clean = re.sub(r"[^\d.]", "", raw_cpc) or "0"
    cpc_num = float(cpc_clean)
    cpc_normalized = min(100.0, (cpc_num / cfg.max_cpc_normalization) * 100.0)

    # Parse SERP features
    try:
        serp_num = float(raw_serp) if raw_serp is not None else 0.0
    except (ValueError, TypeError):
        serp_num = 0.0
    serp_normalized = min(100.0, (serp_num / cfg.max_serp_normalization) * 100.0)

    # Compute composite score
    composite = (
        (volume_normalized * cfg.volume_weight)
        + ((100.0 - difficulty_num) * cfg.difficulty_weight)
        + (cpc_normalized * cfg.cpc_weight)
        + (serp_normalized * cfg.serp_features_weight)
    )

    return round(max(0.0, min(100.0, composite)))


class OpportunityScorerService:
    """Service for batch opportunity scoring and tracking score delta shifts."""

    def __init__(self, config: OpportunityScorerConfig | None = None) -> None:
        self._config = config or OpportunityScorerConfig()
        # In-memory history for alert tracking: (tenant_id, keyword) -> last_score
        self._history: dict[tuple[str, str], int] = {}
        self._alerts: list[OpportunityAlert] = []

    def score_keywords(
        self, tenant_id: str, keywords: list[ReportKeyword]
    ) -> tuple[list[OpportunityScore], list[OpportunityAlert]]:
        """Score keyword set and trigger alerts if score delta exceeds threshold."""
        scores: list[OpportunityScore] = []
        new_alerts: list[OpportunityAlert] = []

        for kw in keywords:
            calculated = calculate_opportunity_score(kw, self._config)
            key = (tenant_id, kw.keyword)
            prev_score = self._history.get(key)

            if prev_score is not None:
                delta = calculated - prev_score
                if abs(delta) >= 10:
                    alert = OpportunityAlert(
                        id=str(uuid.uuid4())[:8],
                        tenant_id=tenant_id,
                        keyword=kw.keyword,
                        previous_score=prev_score,
                        current_score=calculated,
                        delta=delta,
                        threshold=10,
                        status="open",
                    )
                    new_alerts.append(alert)
                    self._alerts.append(alert)

            self._history[key] = calculated

            scores.append(
                OpportunityScore(
                    keyword=kw.keyword,
                    score=calculated,
                    volume=kw.volume,
                    difficulty=float(kw.difficulty),
                    cpc=kw.cpc,
                    serp_features=int(kw.serp_features),
                )
            )

        return scores, new_alerts

    def get_alerts(self, tenant_id: str) -> list[OpportunityAlert]:
        return [a for a in self._alerts if a.tenant_id == tenant_id]

    def acknowledge_alert(self, tenant_id: str, alert_id: str) -> bool:
        for idx, a in enumerate(self._alerts):
            if a.tenant_id == tenant_id and a.id == alert_id:
                self._alerts[idx] = OpportunityAlert(
                    id=a.id,
                    tenant_id=a.tenant_id,
                    keyword=a.keyword,
                    previous_score=a.previous_score,
                    current_score=a.current_score,
                    delta=a.delta,
                    threshold=a.threshold,
                    status="acknowledged",
                )
                return True
        return False
