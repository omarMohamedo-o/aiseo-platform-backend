"""FastAPI routes for AI Model configuration."""

from __future__ import annotations

from apps.admin_api.app.api.dependencies import require_superadmin
from apps.admin_api.app.application.ai_config_service import AiConfigService
from apps.admin_api.app.domain.admin_user import AdminUser
from apps.admin_api.app.domain.platform_config import PlatformConfig
from apps.admin_api.app.infrastructure.repositories.in_memory_platform_repo import (
    InMemoryPlatformConfigRepository,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/admin/ai", tags=["AI Config"])

# In real app, these would be injected by a DI container
config_repo = InMemoryPlatformConfigRepository()
config_service = AiConfigService(config_repo)


class UpdateRoutingRequest(BaseModel):
    task_type: str
    target_model: str


@router.get("/config")
async def get_platform_config(
    admin: AdminUser = Depends(require_superadmin),
) -> PlatformConfig:
    """Get the current global AI routing and scoring configuration."""
    return await config_repo.get_latest()


@router.put("/routes")
async def update_ai_route(
    payload: UpdateRoutingRequest,
    admin: AdminUser = Depends(require_superadmin),
) -> PlatformConfig:
    """Update which AI model handles a specific task (e.g. switch to DeepSeek)."""
    return await config_service.update_routing_rule(
        task_type=payload.task_type,
        target_model=payload.target_model,
        admin=admin,
    )
