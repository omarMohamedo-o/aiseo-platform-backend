"""API routes for keyword search trends."""
from __future__ import annotations

import json
import urllib.request

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import get_trends_adapter
from aiseo.ports.trends.trends_port import TrendSeriesResult, TrendsPort

router = APIRouter(prefix="/api/v1/trends", tags=["trends"])


class TrendsQueryRequest(BaseModel):
    terms: list[str] = Field(min_length=1, max_length=10)
    geo: str = "WORLDWIDE"
    start_date: str = "12 months ago"
    category: str = "all"


@router.post("/series", response_model=TrendSeriesResult)
async def fetch_trends_series(
    payload: TrendsQueryRequest,
    trends_adapter: TrendsPort = Depends(get_trends_adapter),
) -> TrendSeriesResult:
    return await trends_adapter.fetch_trends(
        terms=payload.terms,
        geo=payload.geo,
        start_date=payload.start_date,
        category=payload.category,
    )

@router.get("/live-breakouts")
async def get_live_breakouts():
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5.0)
            ids = resp.json()[:8]
            
            breakouts = []
            for i in ids:
                item_resp = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5.0)
                item = item_resp.json()
            # Basic categorization
            title = item.get("title", "")
            cat = "Tech"
            if "AI" in title or "GPT" in title or "LLM" in title:
                cat = "AI"
            elif "API" in title or "Code" in title or "HN" in title:
                cat = "Developer Tools"
            elif "startup" in title.lower() or "funding" in title.lower():
                cat = "FinTech"
                
            breakouts.append({
                "term": title[:40] + ("..." if len(title) > 40 else ""),
                "type": cat
            })
        return {"breakouts": breakouts}
    except Exception:
        return {"breakouts": [
            {"term": "AI Optimization", "type": "Tech"},
            {"term": "Python 3.12", "type": "Developer Tools"}
        ]}
