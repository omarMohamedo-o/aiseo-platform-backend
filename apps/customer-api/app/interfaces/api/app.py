"""FastAPI application factory for the Customer API.

This builds the public-facing API that the client's Next.js dashboard talks to.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from apps.customer_api.app.interfaces.api.routes.changes import router as changes_router
from apps.customer_api.app.interfaces.api.routes.scans import router as scans_router

# Correct imports from the new bounded context structure
from apps.customer_api.app.interfaces.api.routes.websites import router as websites_router
from fastapi import FastAPI


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Setup logic (e.g. initializing DB pools) goes here
        yield
        # Teardown logic goes here

    app = FastAPI(
        title="Enterprise GEO Platform - Customer API",
        description="Public API consumed by the customer dashboard.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Register routers
    app.include_router(websites_router)
    app.include_router(scans_router)
    app.include_router(changes_router)

    @app.get("/health", tags=["System"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "customer-api"}

    return app
