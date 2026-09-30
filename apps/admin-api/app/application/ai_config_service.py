"""Application service for managing global platform configuration and AI routes."""

from __future__ import annotations

from typing import Protocol

from apps.admin_api.app.domain.admin_user import AdminUser
from apps.admin_api.app.domain.platform_config import PlatformConfig


class PlatformConfigRepository(Protocol):
    """Protocol for persisting platform configuration."""

    async def get_latest(self) -> PlatformConfig: ...

    async def save(self, config: PlatformConfig) -> None: ...


class AiConfigService:
    """Use cases for managing AI routing and configuration."""

    def __init__(self, config_repo: PlatformConfigRepository) -> None:
        self._config_repo = config_repo

    async def update_routing_rule(
        self,
        task_type: str,
        target_model: str,
        admin: AdminUser,
    ) -> PlatformConfig:
        """Update the active AI model for a specific task."""

        if not admin.can_manage_config():
            raise PermissionError("Admin does not have permissions to manage AI routing.")

        config = await self._config_repo.get_latest()

        # Apply the update
        updated_config = config.update_routing_rule(
            task=task_type,
            target_model=target_model,
            admin_id=admin.id,
        )

        # Save to DB
        await self._config_repo.save(updated_config)

        # Note: In a real distributed system, we would publish an Event here
        # so the Recommendation Service (AI Gateway) updates its in-memory router.

        return updated_config
