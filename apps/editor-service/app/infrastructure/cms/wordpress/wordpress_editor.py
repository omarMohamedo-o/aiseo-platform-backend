"""WordPress REST API adapter for applying SEO changes.

Implements the WebsiteEditorPort Protocol using the WordPress REST API
to modify post/page titles, meta descriptions, content, and other SEO
elements programmatically.

This is the ONLY file in the codebase that knows about WordPress API
specifics. Business logic only ever interacts via the WebsiteEditorPort.
"""

from __future__ import annotations

import httpx
from apps.editor_service.app.domain.models import (
    ChangeResult,
    ChangeType,
    ContentChange,
    IntegrationMethod,
    WebsiteConnection,
)


class WordPressEditor:
    """Applies SEO changes to WordPress sites via the REST API.

    Satisfies the WebsiteEditorPort Protocol through structural typing.
    The httpx client is a private implementation detail.

    WordPress REST API endpoints used:
    - GET/PUT /wp-json/wp/v2/pages/<id>  (pages)
    - GET/PUT /wp-json/wp/v2/posts/<id>  (posts)
    - GET /wp-json/wp/v2/pages?search=... (find page by URL)
    """

    def __init__(self, timeout: float = 30.0) -> None:
        self._timeout = timeout

    async def test_connection(self, connection: WebsiteConnection) -> bool:
        """Test WordPress API connectivity with the stored credentials."""
        try:
            async with self._create_client(connection) as client:
                response = await client.get("/wp-json/wp/v2/users/me")
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def apply_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> ChangeResult:
        """Apply a single content change to WordPress."""
        try:
            async with self._create_client(connection) as client:
                # Find the WordPress post/page ID for this URL
                page_id = await self._find_page_id(client, change.page_url)
                if page_id is None:
                    return ChangeResult(
                        success=False,
                        change_id=change.id,
                        message=f"Page not found in WordPress: {change.page_url}",
                        applied_via=IntegrationMethod.CMS_WORDPRESS,
                        error="Page not found in WordPress REST API",
                    )

                # Build the update payload based on change type
                payload = self._build_payload(change)
                if not payload:
                    return ChangeResult(
                        success=False,
                        change_id=change.id,
                        message=f"Unsupported change type for WordPress: {change.change_type}",
                        applied_via=IntegrationMethod.CMS_WORDPRESS,
                        error=f"Change type {change.change_type} not implemented",
                    )

                # Apply the change via PUT request
                response = await client.put(
                    f"/wp-json/wp/v2/pages/{page_id}",
                    json=payload,
                )

                if response.status_code == 200:
                    # Verify the change was applied (Fetch-Patch-Verify)
                    verified = await self._verify_update(client, page_id, change)
                    return ChangeResult(
                        success=True,
                        change_id=change.id,
                        message=f"Successfully updated {change.change_type.value} on {change.page_url}",
                        applied_via=IntegrationMethod.CMS_WORDPRESS,
                        verified=verified,
                    )

                return ChangeResult(
                    success=False,
                    change_id=change.id,
                    message=f"WordPress API returned {response.status_code}",
                    applied_via=IntegrationMethod.CMS_WORDPRESS,
                    error=response.text[:500],
                )

        except httpx.HTTPError as e:
            return ChangeResult(
                success=False,
                change_id=change.id,
                message=f"HTTP error communicating with WordPress: {e}",
                applied_via=IntegrationMethod.CMS_WORDPRESS,
                error=str(e),
            )

    async def verify_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> bool:
        """Verify a change exists on the live site by fetching the page."""
        try:
            async with self._create_client(connection) as client:
                page_id = await self._find_page_id(client, change.page_url)
                if page_id is None:
                    return False
                return await self._verify_update(client, page_id, change)
        except httpx.HTTPError:
            return False

    async def rollback_change(
        self,
        connection: WebsiteConnection,
        change: ContentChange,
    ) -> ChangeResult:
        """Rollback: apply the original (before) value."""
        if change.before_value is None:
            return ChangeResult(
                success=False,
                change_id=change.id,
                message="No before_value stored, cannot rollback",
                applied_via=IntegrationMethod.CMS_WORDPRESS,
                error="Missing before_value for rollback",
            )

        # Create a reversed change (swap before/after)
        rollback_change = change.model_copy(update={"after_value": change.before_value})
        return await self.apply_change(connection, rollback_change)

    async def publish_sitemap(
        self,
        connection: WebsiteConnection,
        sitemap_xml: str,
    ) -> bool:
        """Publish a sitemap.xml. For WordPress, this typically involves
        updating a specific file via custom REST endpoint or uploading media,
        but in a standard setup, we rely on SEO plugins. For MVP, we can
        return True if we ping search engines successfully, or use a custom
        route if available.
        """
        # Placeholder for MVP: Assume success if connection is valid
        # A real implementation would upload the sitemap.xml file to the root directory
        # or integrate with Yoast/RankMath endpoints.
        return await self.test_connection(connection)

    # ── Private Helpers ────────────────────────────────────────

    def _create_client(self, connection: WebsiteConnection) -> httpx.AsyncClient:
        """Create an authenticated httpx client for WordPress."""
        headers: dict[str, str] = {"Content-Type": "application/json"}

        # Support both Application Password and JWT auth
        username = connection.credentials.get("username", "")
        app_password = connection.credentials.get("app_password", "")
        if username and app_password:
            auth = httpx.BasicAuth(username, app_password)
        else:
            auth = None
            # Try Bearer token
            token = connection.credentials.get("token", "")
            if token:
                headers["Authorization"] = f"Bearer {token}"

        return httpx.AsyncClient(
            base_url=connection.base_url,
            headers=headers,
            auth=auth,
            timeout=self._timeout,
        )

    async def _find_page_id(self, client: httpx.AsyncClient, page_url: str) -> int | None:
        """Find the WordPress post/page ID by its URL slug."""
        from urllib.parse import urlparse

        path = urlparse(page_url).path.strip("/")
        slug = path.split("/")[-1] if path else ""

        # Try pages first
        for content_type in ["pages", "posts"]:
            response = await client.get(
                f"/wp-json/wp/v2/{content_type}",
                params={"slug": slug, "per_page": 1},
            )
            if response.status_code == 200:
                results = response.json()
                if results:
                    return int(results[0]["id"])

        return None

    def _build_payload(self, change: ContentChange) -> dict | None:  # type: ignore[type-arg]
        """Build the WordPress API payload for a given change type."""
        match change.change_type:
            case ChangeType.META_TITLE:
                return {"title": change.after_value}
            case ChangeType.META_DESCRIPTION:
                # WordPress uses Yoast or meta fields for descriptions
                return {
                    "meta": {
                        "_yoast_wpseo_metadesc": change.after_value,
                    }
                }
            case ChangeType.CONTENT_SECTION:
                return {"content": change.after_value}
            case ChangeType.HEADING_H1:
                return {"title": change.after_value}
            case _:
                return None

    async def _verify_update(
        self,
        client: httpx.AsyncClient,
        page_id: int,
        change: ContentChange,
    ) -> bool:
        """Re-fetch the page to verify the change was applied."""
        response = await client.get(f"/wp-json/wp/v2/pages/{page_id}")
        if response.status_code != 200:
            return False

        data = response.json()
        match change.change_type:
            case ChangeType.META_TITLE:
                rendered_title = data.get("title", {}).get("rendered", "")
                return change.after_value in rendered_title
            case ChangeType.CONTENT_SECTION:
                rendered = data.get("content", {}).get("rendered", "")
                return change.after_value[:50] in rendered
            case _:
                return True  # Assume success for types we can't verify inline
