import uuid

from aiseo.domain.value_objects import TenantId, Url
from aiseo.domain.websites.website import Website, WebsiteStatus


def _tenant() -> TenantId:
    return TenantId(value=uuid.uuid4())


def test_register_creates_website_in_registered_state() -> None:
    website = Website.register(tenant_id=_tenant(), url=Url(value="https://example.com"))
    assert website.status == WebsiteStatus.REGISTERED


def test_start_crawl_transitions_state_and_is_immutable() -> None:
    website = Website.register(tenant_id=_tenant(), url=Url(value="https://example.com"))
    crawling = website.start_crawl()

    assert crawling.status == WebsiteStatus.CRAWLING
    assert website.status == WebsiteStatus.REGISTERED  # original untouched
    assert crawling.id == website.id


def test_complete_crawl_and_fail_transitions() -> None:
    website = Website.register(tenant_id=_tenant(), url=Url(value="https://example.com"))
    crawled = website.start_crawl().complete_crawl()
    assert crawled.status == WebsiteStatus.CRAWLED

    failed = website.start_crawl().fail()
    assert failed.status == WebsiteStatus.FAILED
