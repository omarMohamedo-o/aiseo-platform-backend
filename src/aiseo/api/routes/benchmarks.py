"""Global AI Visibility Benchmark and Leaderboard API."""
from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel

from aiseo.infrastructure.database.history_repo import get_history

router = APIRouter(prefix="/api/v1/benchmarks", tags=["benchmarks"])

class LeaderboardEntry(BaseModel):
    rank: int
    domain: str
    brand_name: str
    category: str
    country: str
    visibility_score: int
    opportunity_score: int
    seo_score: int
    aeo_score: int
    geo_score: int
    glmm_score: int
    citation_share: float
    schema_score: int
    direct_answer_score: int
    total_pages_indexed: int
    top_query: str
    growth_trend: str
    search_rank: float
    ai_search_rank: int
    monthly_search_volume: int
    monthly_unique_searchers: int
    search_appearances: int
    ai_answer_appearances: int
    avg_cpc: float
    keyword_difficulty: int
    organic_ctr: float
    estimated_monthly_traffic: int

class IndustryAverage(BaseModel):
    category: str
    avg_visibility: int
    avg_opportunity: int
    total_audited_domains: int

class GlobalBenchmarkResponse(BaseModel):
    last_updated: str
    total_global_domains_tracked: int
    leaderboard: list[LeaderboardEntry]
    industry_averages: list[IndustryAverage]
    engine_citation_shares: dict[str, float]


@router.get("/global-leaderboard", response_model=GlobalBenchmarkResponse)
async def get_global_leaderboard(
    category: str | None = Query(default=None, description="Optional category filter"),
    sort_by: str = Query(default="overall", description="Sort by overall, seo, aeo, geo, glmm"),
) -> GlobalBenchmarkResponse:
    # 1. Initialize combined dict
    combined_dict = {}

    # 2. Add real audit history from HistoryDB
    history = get_history()
    for item in history:
        vis_score = item.get("visibility_score", 0)
        opp_score = item.get("opportunity_score", 0)
        
        # Real extracted readiness scores if available
        result_payload = item.get("result_payload", {})
        readiness = result_payload.get("readiness_scores", {})
        seo = readiness.get("SEO", 0)
        aeo = readiness.get("AEO", 0)
        geo = readiness.get("GEO", 0)
        glmm = readiness.get("GLMM", 0)
        
        brand = item.get("brand_name", "") or "Unknown"
        raw_url = item.get("url", "")
        if not raw_url:
            continue
            
        # Clean domain
        domain = raw_url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].lower()
        
        combined_dict[domain] = LeaderboardEntry(
            rank=0,
            domain=domain,
            brand_name=brand,
            category="Audited Domain",
            country="Global",
            visibility_score=vis_score,
            opportunity_score=opp_score,
            seo_score=seo,
            aeo_score=aeo,
            geo_score=geo,
            glmm_score=glmm,
            citation_share=0.0,
            schema_score=0,
            direct_answer_score=0,
            total_pages_indexed=0,
            top_query="",
            growth_trend="+0.0%",
            search_rank=0.0,
            ai_search_rank=0,
            monthly_search_volume=0,
            monthly_unique_searchers=0,
            search_appearances=0,
            ai_answer_appearances=0,
            avg_cpc=0.0,
            keyword_difficulty=0,
            organic_ctr=0.0,
            estimated_monthly_traffic=0,
        )

    # 3. Sort by the requested metric to dynamically generate ranks
    leaderboard_data = list(combined_dict.values())
    if sort_by == "seo":
        leaderboard_data.sort(key=lambda x: x.seo_score, reverse=True)
    elif sort_by == "aeo":
        leaderboard_data.sort(key=lambda x: x.aeo_score, reverse=True)
    elif sort_by == "geo":
        leaderboard_data.sort(key=lambda x: x.geo_score, reverse=True)
    elif sort_by == "glmm":
        leaderboard_data.sort(key=lambda x: x.glmm_score, reverse=True)
    else:
        leaderboard_data.sort(key=lambda x: x.visibility_score, reverse=True)
    
    # 4. Assign dynamic ranks
    for i, entry in enumerate(leaderboard_data):
        entry.rank = i + 1

    # 5. Apply category filter
    filtered = leaderboard_data
    if category and category.lower() != "all":
        filtered = [e for e in leaderboard_data if e.category.lower() == category.lower()]

    # 6. Recalculate industry averages dynamically
    category_stats = {}
    for entry in leaderboard_data:
        if entry.category not in category_stats:
            category_stats[entry.category] = {"vis": 0, "opp": 0, "count": 0}
        category_stats[entry.category]["vis"] += entry.visibility_score
        category_stats[entry.category]["opp"] += entry.opportunity_score
        category_stats[entry.category]["count"] += 1

    dynamic_averages = []
    for cat, stats in category_stats.items():
        dynamic_averages.append(IndustryAverage(
            category=cat,
            avg_visibility=round(stats["vis"] / stats["count"]),
            avg_opportunity=round(stats["opp"] / stats["count"]),
            total_audited_domains=stats["count"],
        ))

    return GlobalBenchmarkResponse(
        last_updated=datetime.now(UTC).isoformat(),
        total_global_domains_tracked=len(leaderboard_data),
        leaderboard=filtered,
        industry_averages=dynamic_averages,
        engine_citation_shares={
            "ChatGPT (Search & Browse)": 38.4,
            "Perplexity AI": 31.2,
            "Claude (Anthropic)": 17.6,
            "Google Gemini": 12.8,
        },
    )
