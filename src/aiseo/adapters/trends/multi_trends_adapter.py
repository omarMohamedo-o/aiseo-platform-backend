"""Multi-provider Trends adapter for keyword velocity and interest over time."""
from __future__ import annotations

import asyncio
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta

from pytrends.request import TrendReq

from aiseo.ports.trends.trends_port import TrendPoint, TrendSeriesResult, TrendsPort


class MultiTrendsAdapter(TrendsPort):
    """Fetches and normalizes keyword search trend time-series data using multiple free providers."""

    def __init__(self, *args, **kwargs) -> None:
        self.executor = ThreadPoolExecutor(max_workers=3)

    def _fetch_pytrends(self, terms: list[str]) -> list[TrendPoint]:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(terms, cat=0, timeframe='today 1-m', geo='', gprop='')
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

    def _fetch_wikipedia(self, terms: list[str]) -> list[TrendPoint]:
        # Fetch 30 days of wikipedia page views
        start = (datetime.now(UTC) - timedelta(days=30)).strftime('%Y%m%d')
        end = datetime.now(UTC).strftime('%Y%m%d')
        
        # We will collect views for each term per day
        date_map = {}
        for i in range(31):
            d = (datetime.now(UTC) - timedelta(days=i)).strftime('%Y-%m-%d')
            date_map[d] = {t: 0.0 for t in terms}
            
        for term in terms:
            # clean term for wikipedia title
            wiki_title = term.replace(' ', '_').capitalize()
            url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{wiki_title}/daily/{start}/{end}'
            req = urllib.request.Request(url, headers={'User-Agent': 'AISEOPlatform/1.0'})
            try:
                resp = urllib.request.urlopen(req, timeout=5)
                data = json.loads(resp.read())
                
                # Normalize values to a 0-100 scale for consistency with trends
                max_views = max([int(item.get('views', 0)) for item in data.get('items', [])] + [1])
                
                for item in data.get('items', []):
                    timestamp = item.get('timestamp', '')[:8]
                    if len(timestamp) == 8:
                        d_str = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}"
                        views = int(item.get('views', 0))
                        if d_str in date_map:
                            date_map[d_str][term] = (views / max_views) * 100.0
            except Exception as e:
                print(f"Wiki fetch failed for {term}: {e}")
                
        # Return sorted by date
        points = []
        for d in sorted(date_map.keys()):
            points.append(TrendPoint(date=d, values=date_map[d]))
            
        # Check if we got any real data
        has_data = any(val > 0 for p in points for val in p.values.values())
        if not has_data:
            return []
            
        return points

    def _fetch_sync(self, terms: list[str]) -> tuple[str, list[TrendPoint]]:
        # 1. Try PyTrends first
        try:
            pts = self._fetch_pytrends(terms)
            if pts:
                return "Google Trends", pts
        except Exception as e:
            print("PyTrends failed:", e)
            
        # 2. Try Wikipedia Page Views
        try:
            pts = self._fetch_wikipedia(terms)
            if pts:
                return "Wikipedia Pageviews API", pts
        except Exception as e:
            print("Wikipedia failed:", e)
            
        # 3. If all fail, return empty
        return "None", []

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
            provider_name, points = await loop.run_in_executor(self.executor, self._fetch_sync, terms)
            
            return TrendSeriesResult(
                configured=True,
                provider=provider_name,
                fetched_at=now_str,
                terms=terms,
                points=points,
            )
        except Exception as exc:
            return TrendSeriesResult(
                configured=False,
                provider="Multi-Provider Fallback",
                fetched_at=now_str,
                terms=terms,
                points=[],
                message=f"All trend providers failed: {exc}",
            )
