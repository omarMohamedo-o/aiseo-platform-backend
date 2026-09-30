"""Main entrypoint for the Admin Control Plane API."""

from apps.admin_api.app.api.routes import ai_models, tenants
from fastapi import FastAPI

app = FastAPI(
    title="GEO Platform - Admin Control Plane",
    description="Internal API for managing AI models, scoring configurations, and tenants.",
    version="1.0.0",
)

app.include_router(ai_models.router)
app.include_router(tenants.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "admin-api"}
