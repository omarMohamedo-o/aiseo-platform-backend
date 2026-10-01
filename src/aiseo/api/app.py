"""FastAPI application factory. This is where the composition root meets
the web framework -- the only place infrastructure is constructed at startup."""
from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from aiseo.api.routes.auth import router as auth_router
from aiseo.api.routes.benchmarks import router as benchmarks_router
from aiseo.api.routes.intelligence import router as intelligence_router
from aiseo.api.routes.reports import router as reports_router
from aiseo.api.routes.trends import router as trends_router
from aiseo.api.routes.vault import router as vault_router
from aiseo.api.routes.visibility import router as visibility_router
from aiseo.api.routes.websites import router as websites_router
from aiseo.infrastructure.configuration.composition_root import build_container
from aiseo.infrastructure.configuration.settings import Settings
from aiseo.infrastructure.observability.logging import configure_logging, get_logger


def create_app(settings: Settings | None = None) -> FastAPI:
    container = build_container(settings)
    configure_logging(container.settings.environment)
    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        app.state.container = container
        logger.info("aiseo.startup", environment=container.settings.environment)
        yield
        logger.info("aiseo.shutdown")

    app = FastAPI(
        title="Enterprise AI SEO/AEO/GEO Platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Enable CORS for frontend development and dashboard interactions
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(websites_router)
    app.include_router(benchmarks_router)
    app.include_router(intelligence_router)
    app.include_router(visibility_router)
    app.include_router(trends_router)
    app.include_router(auth_router)
    app.include_router(reports_router)
    app.include_router(vault_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    # Serve the frontend
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "frontend", "web", "dist")
    if os.path.exists(frontend_dist):
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
        
        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            if full_path.startswith("api/"):
                return {"error": "Not found"}
            return FileResponse(os.path.join(frontend_dist, "index.html"))

    return app
