import uuid

import pytest

from aiseo.adapters.persistence.in_memory_website_repository import InMemoryWebsiteRepository
from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.domain.value_objects import TenantId, Url


@pytest.mark.asyncio
async def test_register_website_is_idempotent_for_same_url() -> None:
    repo = InMemoryWebsiteRepository()
    service = RegisterWebsiteService(website_repository=repo)
    tenant_id = TenantId(value=uuid.uuid4())
    url = Url(value="https://example.com")

    first = await service.register(tenant_id, url)
    second = await service.register(tenant_id, url)

    assert first.id == second.id
    assert len(await repo.list_for_tenant(tenant_id)) == 1


@pytest.mark.asyncio
async def test_register_website_enforces_tenant_isolation() -> None:
    repo = InMemoryWebsiteRepository()
    service = RegisterWebsiteService(website_repository=repo)
    tenant_a = TenantId(value=uuid.uuid4())
    tenant_b = TenantId(value=uuid.uuid4())
    url = Url(value="https://example.com")

    await service.register(tenant_a, url)

    assert await repo.get_by_url(tenant_b, url) is None
    assert len(await repo.list_for_tenant(tenant_b)) == 0
