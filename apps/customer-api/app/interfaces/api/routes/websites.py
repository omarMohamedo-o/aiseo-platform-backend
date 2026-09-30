"""Website registration API, v1."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from aiseo.api.dependencies.container import get_register_website_service
from aiseo.api.dependencies.tenant import get_current_tenant
from aiseo.api.schemas.website_schemas import RegisterWebsiteRequest, WebsiteResponse
from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.domain.errors import InvalidUrlError
from aiseo.domain.value_objects import TenantId, Url

router = APIRouter(prefix="/api/v1/websites", tags=["websites"])


@router.post("", response_model=WebsiteResponse, status_code=201)
async def register_website(
    payload: RegisterWebsiteRequest,
    tenant_id: TenantId = Depends(get_current_tenant),
    service: RegisterWebsiteService = Depends(get_register_website_service),
) -> WebsiteResponse:
    try:
        url = Url(value=payload.url)
    except InvalidUrlError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    website = await service.register(tenant_id=tenant_id, url=url)
    return WebsiteResponse.from_domain(website)
