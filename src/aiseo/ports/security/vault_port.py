"""Encrypted secret vault capability port."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict


class StoredCredential(BaseModel):
    """Decrypted integration credential."""

    model_config = ConfigDict(frozen=True)

    provider: str
    api_url: str
    api_key: str
    model: str = ""
    updated_at: str | None = None


@runtime_checkable
class VaultPort(Protocol):
    """Protocol for storing and retrieving workspace/tenant-scoped encrypted credentials."""

    async def save_credentials(
        self,
        tenant_id: str,
        provider: str,
        api_url: str,
        api_key: str,
        model: str = "",
    ) -> None:
        """Securely encrypt and persist integration credentials."""
        ...

    async def get_credentials(
        self, tenant_id: str, provider: str
    ) -> StoredCredential | None:
        """Retrieve and decrypt integration credentials for a specific tenant and provider."""
        ...

    async def delete_credentials(self, tenant_id: str, provider: str) -> None:
        """Delete stored integration credentials."""
        ...
