"""API routes for workspace-scoped encrypted credentials vault."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import get_vault
from aiseo.ports.security.vault_port import VaultPort

router = APIRouter(prefix="/api/v1/vault", tags=["vault"])


def _extract_tenant(x_tenant_id: str | None = Header(default="default-tenant")) -> str:
    return x_tenant_id or "default-tenant"


def _mask_secret(secret: str) -> str:
    if not secret or len(secret) <= 6:
        return "••••••"
    return f"{secret[:3]}••••••{secret[-3:]}"


class SaveCredentialRequest(BaseModel):
    provider: str
    api_url: str
    api_key: str = Field(min_length=6)
    model: str = ""


class ProviderStatusResponse(BaseModel):
    provider: str
    configured: bool
    api_url: str
    masked_key: str
    model: str


@router.get("/status", response_model=list[ProviderStatusResponse])
async def list_providers_status(
    tenant_id: str = Depends(_extract_tenant),
    vault: VaultPort = Depends(get_vault),
) -> list[ProviderStatusResponse]:
    known_providers = ["openai", "gemini", "claude", "perplexity", "google-trends", "report-email"]
    statuses: list[ProviderStatusResponse] = []

    for p in known_providers:
        cred = await vault.get_credentials(tenant_id, p)
        statuses.append(
            ProviderStatusResponse(
                provider=p,
                configured=cred is not None,
                api_url=cred.api_url if cred else "",
                masked_key=_mask_secret(cred.api_key) if cred else "",
                model=cred.model if cred else "",
            )
        )
    return statuses


@router.post("/credentials")
async def save_credential(
    payload: SaveCredentialRequest,
    tenant_id: str = Depends(_extract_tenant),
    vault: VaultPort = Depends(get_vault),
) -> dict[str, bool]:
    await vault.save_credentials(
        tenant_id=tenant_id,
        provider=payload.provider,
        api_url=payload.api_url,
        api_key=payload.api_key,
        model=payload.model,
    )
    return {"success": True}


@router.delete("/credentials/{provider}")
async def delete_credential(
    provider: str,
    tenant_id: str = Depends(_extract_tenant),
    vault: VaultPort = Depends(get_vault),
) -> dict[str, bool]:
    await vault.delete_credentials(tenant_id=tenant_id, provider=provider)
    return {"success": True}
