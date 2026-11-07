"""Anti-scraping, bot defense, and rate-limiting middleware.

Provides defense-in-depth against automated content scraping, scraper bots,
and unauthenticated rate abuses across proprietary benchmark & audit endpoints.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class AntiScrapingMiddleware(BaseHTTPMiddleware):
    """Enforces scraping protection, rate-limiting, and bot fingerprint detection."""

    # Programmatic scrapers and headless bots
    BLOCKED_USER_AGENTS = (
        "scrapy",
        "python-requests",
        "aiohttp",
        "wget",
        "curl/",
        "go-http-client",
        "httpclient",
        "bytespider",
        "headlesschrome",
        "phantomjs",
        "selenium",
        "puppeteer",
    )

    # Protected endpoints requiring anti-scraping vigilance
    PROTECTED_PREFIXES = (
        "/api/v1/websites/matrix-benchmark",
        "/api/v1/websites/crawl-and-analyze",
        "/api/v1/websites/discover-competitors",
    )

    def __init__(self, app, max_requests_per_minute: int = 15) -> None:
        super().__init__(app)
        self.max_requests_per_minute = max_requests_per_minute
        self.request_history: dict[str, list[float]] = defaultdict(list)
        self.blacklisted_ips: set[str] = set()

    def _get_client_ip(self, request: Request) -> str:
        # Check standard forwarding headers from proxies / Vercel
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = self._get_client_ip(request)
        path = request.url.path

        # 1. Honeypot Trap Detection
        if path == "/api/v1/security/honeypot":
            self.blacklisted_ips.add(client_ip)
            return JSONResponse(
                status_code=403,
                content={"error": "Access denied: automated scraping bot trap triggered"},
            )

        # 2. Check Blacklisted IPs
        if client_ip in self.blacklisted_ips:
            return JSONResponse(
                status_code=403,
                content={"error": "Access denied: client IP blacklisted for scraping abuse"},
            )

        # Only apply deep checks to API routes
        if path.startswith("/api/"):
            user_agent = request.headers.get("user-agent", "").lower()

            # 3. Known Automated Scraper Blacklist
            for blocked_agent in self.BLOCKED_USER_AGENTS:
                if blocked_agent in user_agent:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": "Access denied: automated scraping tool detected",
                            "agent": blocked_agent,
                        },
                    )

            # 4. Rate Limiting for Public Audit Endpoints
            if any(path.startswith(prefix) for prefix in self.PROTECTED_PREFIXES):
                now = time.time()
                history = self.request_history[client_ip]

                # Filter out requests older than 60 seconds
                self.request_history[client_ip] = [ts for ts in history if now - ts < 60]

                if len(self.request_history[client_ip]) >= self.max_requests_per_minute:
                    return JSONResponse(
                        status_code=429,
                        headers={"Retry-After": "60"},
                        content={
                            "error": "Rate limit exceeded: maximum 15 audit queries per minute per IP",
                            "retry_after_seconds": 60,
                        },
                    )

                self.request_history[client_ip].append(now)

        return await call_next(request)
