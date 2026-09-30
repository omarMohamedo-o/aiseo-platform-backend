"""In-memory repositories for Admin API (MVP)."""

from __future__ import annotations

import uuid

from apps.admin_api.app.domain.platform_config import PlatformConfig


class InMemoryPlatformConfigRepository:
    """Mock repository for storing the global platform configuration."""

    def __init__(self) -> None:
        # Initialize with default config
        self._config = PlatformConfig(id=uuid.uuid4())

    async def get_latest(self) -> PlatformConfig:
        return self._config

    async def save(self, config: PlatformConfig) -> None:
        self._config = config
