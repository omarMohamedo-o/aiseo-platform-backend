"""Concrete Ground Truth verification adapter using free, open-source, public APIs.

Connects directly to:
1. Google Suggest (Official public autocomplete API)
2. Wikidata & Wikipedia REST API (Official public entity knowledge graph)
3. DuckDuckGo Instant Answer API (Open search answer engine)
Requires zero paid API keys and zero proprietary subscriptions.
"""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import httpx
import structlog

from aiseo.domain.evaluation.ground_truth import (
    DuckDuckGoEvidence,
    GoogleSuggestEvidence,
    GroundTruthValidationResult,
    WikidataEntityEvidence,
)
from aiseo.ports.evaluation.ground_truth_port import GroundTruthPort

logger = structlog.get_logger(__name__)


class FreeGroundTruthAdapter(GroundTruthPort):
    """Verifies domain and brand authority against free Google, Wikidata, and DuckDuckGo endpoints."""

    def __init__(self, timeout: float = 6.0) -> None:
        self.timeout = timeout
        self.headers = {
            "User-Agent": "AISEO-GroundTruth-Validator/2.0 (compatible; Empirical-Auditor; contact@aiseo.com)",
            "Accept": "application/json",
        }

    async def _fetch_google_suggest(
        self, client: httpx.AsyncClient, brand: str, keyword: str | None = None
    ) -> GoogleSuggestEvidence:
        query = f"{brand} {keyword}".strip() if keyword else brand
        url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={httpx.URL(query)}"

        try:
            resp = await client.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                raw_suggestions = data[1] if len(data) > 1 and isinstance(data[1], list) else []
                suggestions = [str(s) for s in raw_suggestions]
                has_assoc = any(brand.lower() in s.lower() for s in suggestions)
                score = min(100, len(suggestions) * 12 + (20 if has_assoc else 0))
                return GoogleSuggestEvidence(
                    query=query,
                    suggestions=suggestions[:8],
                    has_brand_association=has_assoc,
                    consensus_score=score,
                )
        except Exception as exc:
            logger.debug("Google Suggest query failed", error=str(exc))

        return GoogleSuggestEvidence(query=query, suggestions=[], has_brand_association=False, consensus_score=10)

    async def _fetch_wikidata_entity(
        self, client: httpx.AsyncClient, brand: str
    ) -> WikidataEntityEvidence:
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={httpx.URL(brand)}&language=en&format=json"

        try:
            resp = await client.get(url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                search_results = data.get("search", [])
                if search_results and isinstance(search_results, list):
                    top = search_results[0]
                    wikidata_id = top.get("id")
                    label = top.get("label")
                    desc = top.get("description")
                    return WikidataEntityEvidence(
                        brand=brand,
                        entity_found=True,
                        wikidata_id=wikidata_id,
                        label=label,
                        description=desc,
                        knowledge_graph_authority=95 if desc else 70,
                    )
        except Exception as exc:
            logger.debug("Wikidata entity search failed", error=str(exc))

        return WikidataEntityEvidence(brand=brand, entity_found=False, knowledge_graph_authority=15)

    async def _fetch_duckduckgo_answer(
        self, client: httpx.AsyncClient, brand: str
    ) -> DuckDuckGoEvidence:
        url = f"https://api.duckduckgo.com/?q={httpx.URL(brand)}&format=json&no_html=1&skip_disambig=1"

        try:
            resp = await client.get(url, timeout=self.timeout)
            if resp.status_code in (200, 202):
                data = resp.json()
                heading = data.get("Heading", "")
                abstract = data.get("Abstract", "")
                source_url = data.get("AbstractURL", "")
                has_answer = bool(heading or abstract)
                score = 90 if abstract else (50 if heading else 20)
                return DuckDuckGoEvidence(
                    heading=heading,
                    abstract=abstract[:300],
                    source_url=source_url,
                    has_direct_answer=has_answer,
                    concordance_score=score,
                )
        except Exception as exc:
            logger.debug("DuckDuckGo Instant Answer query failed", error=str(exc))

        return DuckDuckGoEvidence(has_direct_answer=False, concordance_score=10)

    async def verify_domain(
        self,
        domain: str,
        brand: str,
        keywords: list[str] | None = None,
    ) -> GroundTruthValidationResult:
        clean_domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].lower()
        clean_brand = brand or clean_domain.split(".")[0].capitalize()
        kw = keywords[0] if keywords else None

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            google_ev, wiki_ev, ddg_ev = await asyncio.gather(
                self._fetch_google_suggest(client, clean_brand, kw),
                self._fetch_wikidata_entity(client, clean_brand),
                self._fetch_duckduckgo_answer(client, clean_brand),
                return_exceptions=False,
            )

        # Weighted empirical confidence
        overall = int(
            google_ev.consensus_score * 0.40
            + wiki_ev.knowledge_graph_authority * 0.35
            + ddg_ev.concordance_score * 0.25
        )

        if overall >= 75:
            verdict = "HIGH_CONFIDENCE_GROUND_TRUTH"
        elif overall >= 45:
            verdict = "MODERATE_CONFIDENCE"
        else:
            verdict = "EMERGING_ENTITY"

        return GroundTruthValidationResult(
            domain=clean_domain,
            brand=clean_brand,
            timestamp=datetime.now(UTC).isoformat(),
            google_search_evidence=google_ev,
            wikidata_evidence=wiki_ev,
            duckduckgo_evidence=ddg_ev,
            overall_empirical_confidence=overall,
            verdict=verdict,
            methodology="100% Free & Open-Source Empirical Verification (Google Suggest + Wikidata + DuckDuckGo)",
        )

