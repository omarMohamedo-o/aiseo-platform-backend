"""Change Planner domain logic.

Analyzes a ScanSnapshot using predefined SEO rules to determine exactly
what needs to be fixed. It outputs a list of "Fix Requests" that the
ContentGenerator will later fulfill using AI.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.editor_service.app.domain.models import ChangePriority, ChangeType
from apps.visibility_service.app.seo.domain.scan_snapshot import ScanSnapshot


@dataclass
class FixRequest:
    """A requirement to fix a specific issue on a specific page."""

    page_url: str
    change_type: ChangeType
    priority: ChangePriority
    description: str
    current_value: str | None = None
    context: str = ""  # Extra info to help the LLM generate a good fix


class ChangePlanner:
    """Analyzes a snapshot and generates rule-based fix requests."""

    def plan_fixes(self, snapshot: ScanSnapshot) -> list[FixRequest]:
        """Iterate over all page audits and generate needed fixes."""
        requests: list[FixRequest] = []

        for page in snapshot.page_audits:
            # 1. Meta Title
            if not page.meta.title:
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.META_TITLE,
                        priority=ChangePriority.CRITICAL,
                        description="Missing meta title",
                        context=f"The page has {page.word_count} words but no title tag.",
                    )
                )
            elif not (30 <= page.meta.title_length <= 60):
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.META_TITLE,
                        priority=ChangePriority.MEDIUM,
                        description=f"Title is suboptimal length ({page.meta.title_length} chars)",
                        current_value=page.meta.title,
                        context="Title should be between 30 and 60 characters.",
                    )
                )

            # 2. Meta Description
            if not page.meta.meta_description:
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.META_DESCRIPTION,
                        priority=ChangePriority.HIGH,
                        description="Missing meta description",
                        context=f"Page has H1: {page.headings.h1_texts[0] if page.headings.h1_texts else 'None'}",
                    )
                )
            elif not (120 <= page.meta.meta_description_length <= 160):
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.META_DESCRIPTION,
                        priority=ChangePriority.MEDIUM,
                        description=f"Meta description is suboptimal length ({page.meta.meta_description_length} chars)",
                        current_value=page.meta.meta_description,
                    )
                )

            # 3. Headings
            if page.headings.h1_count == 0:
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.HEADING_H1,
                        priority=ChangePriority.HIGH,
                        description="Missing H1 tag",
                        context="Generate a strong H1 that summarizes the page.",
                    )
                )

            # 4. Images
            for img_src in page.images.images_without_alt:
                requests.append(
                    FixRequest(
                        page_url=page.url,
                        change_type=ChangeType.IMAGE_ALT_TEXT,
                        priority=ChangePriority.MEDIUM,
                        description="Missing image alt text",
                        current_value=img_src,
                        context="Image URL is provided. Need descriptive alt text.",
                    )
                )

        # 5. Technical (Sitemap)
        if snapshot.technical_audit and not snapshot.technical_audit.has_sitemap:
            requests.append(
                FixRequest(
                    page_url=snapshot.technical_audit.url,
                    change_type=ChangeType.SITEMAP,
                    priority=ChangePriority.HIGH,
                    description="Missing sitemap.xml",
                )
            )

        return requests
