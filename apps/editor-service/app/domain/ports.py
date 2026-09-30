"""Port interface for applying edits to client websites.

Concrete adapters (WordPress, Shopify, Webflow, Edge Workers, JS Snippet)
implement this Protocol structurally. The application layer only depends
on this interface, never on a specific CMS SDK.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from apps.editor_service.app.domain.models import (
    ChangeResult,
    ContentChange,
    WebsiteConnection,
)


@runtime_checkable
class WebsiteEditorPort(Protocol):
    """Interface for applying, verifying, and rolling back content changes."""

    async def test_connection(self, connection: WebsiteConnection) -> bool:
        """Test if the connection credentials are valid."""
        ...

    async def apply_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> ChangeResult:
        """Apply a content change to the client's website."""
        ...

    async def verify_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> bool:
        """Verify that a change was successfully applied by fetching the page."""
        ...

    async def rollback_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> ChangeResult:
        """Rollback a previously applied change to its original value."""
        ...

    async def publish_sitemap(
        self,
        connection: WebsiteConnection,
        sitemap_xml: str,
    ) -> bool:
        """Publish or push an updated sitemap.xml to the website/CMS."""
        ...
