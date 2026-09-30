"""Configuration for crawling and content extraction."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CrawlerConfig(BaseModel):
    """Crawler adapter configuration."""

    timeout_seconds: float = Field(default=10.0, description="HTTP request timeout in seconds")
    max_pages: int = Field(default=10, description="Maximum pages to discover per crawl")
    user_agent: str = Field(default="AISEOBot/1.0", description="User agent string for HTTP requests")
    follow_redirects: bool = Field(default=True, description="Whether to follow HTTP redirects")


class ExtractorConfig(BaseModel):
    """Scraper/Extractor configuration."""

    timeout_seconds: float = Field(default=15.0, description="HTTP request timeout for content scraper")
    include_comments: bool = Field(default=False, description="Whether to include comments in extraction")
    include_tables: bool = Field(default=True, description="Whether to extract structured HTML tables")
    output_format: str = Field(default="markdown", description="Target content extraction format")
