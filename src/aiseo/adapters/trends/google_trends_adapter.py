"""Google Trends adapter for keyword velocity and interest over time using PyTrends."""
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None  # type: ignore[assignment,misc]

from aiseo.ports.trends.trends_port import TrendPoint, TrendSeriesResult, TrendsPort


class GoogleTrendsAdapter(TrendsPort):
    """Fetches and normalizes keyword search trend time-series data using PyTrends."""

    def __init__(self, *args, **kwargs) -> None:
        self.executor = ThreadPoolExecutor(max_workers=3)

    def _fetch_sync(self, terms: list[str]) -> list[TrendPoint]:
        if TrendReq is None:
            return []
        pytrends = TrendReq(hl='en-US', tz=360)
        # timeframe='today 3-m' or 'today 12-m'
        pytrends.build_payload(terms, cat=0, timeframe='today 3-m', geo='', gprop='')
        df = pytrends.interest_over_time()
        
        if df.empty:
            return []
            
        if 'isPartial' in df.columns:
            df = df.drop(columns=['isPartial'])
            
        points = []
        for index, row in df.iterrows():
            date_str = str(index)[:10]
            values_dict = {}
            for term in terms:
                values_dict[term] = float(row.get(term, 0.0))
            points.append(TrendPoint(date=date_str, values=values_dict))
            
        return points

    async def fetch_trends(
        self,
        terms: list[str],
        geo: str = "WORLDWIDE",
        start_date: str = "12 months ago",
        category: str = "all",
    ) -> TrendSeriesResult:
        now_str = datetime.now(UTC).isoformat()

        try:
            loop = asyncio.get_running_loop()
            points = await loop.run_in_executor(self.executor, self._fetch_sync, terms)
            
            return TrendSeriesResult(
                configured=True,
                provider="pytrends",
                fetched_at=now_str,
                terms=terms,
                points=points,
            )
        except Exception as exc:
            return TrendSeriesResult(
                configured=False,
                provider="pytrends",
                fetched_at=now_str,
                terms=terms,
                points=[],
                message=f"Google Trends query failed: {exc}",
            )
