"""Domain models for per-page On-Page SEO audit data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HeadingInfo(BaseModel):
    """Heading tag analysis for a page."""

    model_config = ConfigDict(extra="forbid")

    h1_count: int = 0
    h1_texts: list[str] = []
    h2_count: int = 0
    h3_count: int = 0
    hierarchy_valid: bool = False  # True if H1 -> H2 -> H3 order is logical


class MetaTagInfo(BaseModel):
    """Meta tag extraction for a page."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    title_length: int = 0
    meta_description: str | None = None
    meta_description_length: int = 0
    has_canonical: bool = False
    canonical_url: str | None = None
    has_robots_meta: bool = False
    robots_content: str | None = None  # "index, follow" etc.
    has_open_graph: bool = False
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | None = None
    has_twitter_card: bool = False


class LinkInfo(BaseModel):
    """Link analysis for a page."""

    model_config = ConfigDict(extra="forbid")

    internal_link_count: int = 0
    external_link_count: int = 0
    broken_link_count: int = 0
    broken_links: list[str] = []
    nofollow_count: int = 0


class ImageInfo(BaseModel):
    """Image analysis for a page."""

    model_config = ConfigDict(extra="forbid")

    total_count: int = 0
    with_alt_count: int = 0
    without_alt_count: int = 0
    images_without_alt: list[str] = []  # src URLs of images missing alt

    @property
    def alt_coverage_pct(self) -> float:
        if self.total_count == 0:
            return 100.0
        return round((self.with_alt_count / self.total_count) * 100, 1)


class StructuredDataInfo(BaseModel):
    """Schema.org structured data analysis."""

    model_config = ConfigDict(extra="forbid")

    has_json_ld: bool = False
    has_microdata: bool = False
    schema_types: list[str] = []  # ["Organization", "Product", "FAQ", ...]
    json_ld_blocks: list[dict] = []  # type: ignore[type-arg]
    validation_errors: list[str] = []


class PageSeoAudit(BaseModel):
    """Complete on-page SEO analysis for a single page.

    Contains every data point needed for display, comparison,
    and recommendation generation.
    """

    model_config = ConfigDict(extra="forbid")

    url: str
    status_code: int | None = None

    # Content metrics
    word_count: int = 0
    language: str | None = None

    # Detailed sub-analyses
    meta: MetaTagInfo = MetaTagInfo()
    headings: HeadingInfo = HeadingInfo()
    links: LinkInfo = LinkInfo()
    images: ImageInfo = ImageInfo()
    structured_data: StructuredDataInfo = StructuredDataInfo()

    # Keyword analysis
    primary_keyword: str | None = None
    keyword_density: float | None = None  # Percentage

    # Content freshness
    last_modified: datetime | None = None

    scanned_at: datetime | None = None
