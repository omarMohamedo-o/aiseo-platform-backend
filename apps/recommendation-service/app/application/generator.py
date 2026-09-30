"""Content Generator application service.

Takes FixRequests, formats prompts, calls the AI Gateway (ModelRouter),
and returns fully structured ContentChange objects ready for approval.
"""

from __future__ import annotations

import uuid

from ai.gateway.interfaces.text_model import LlmRequest
from ai.gateway.router import ModelRouter, TaskType
from apps.editor_service.app.domain.models import ContentChange
from apps.recommendation_service.app.domain.planner import FixRequest
from pydantic import BaseModel


class GeneratedFix(BaseModel):
    """The structured response we expect from the LLM."""

    after_value: str
    ai_reasoning: str | None = None


class ContentGenerator:
    """Uses the AI Gateway to generate content for FixRequests."""

    def __init__(self, router: ModelRouter) -> None:
        self._router = router

    async def generate_fixes(
        self,
        website_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scan_id: uuid.UUID,
        requests: list[FixRequest],
    ) -> list[ContentChange]:
        """Generate AI content for all requests and return ContentChanges."""

        # Get the configured model for content generation
        # The router ensures we don't care if it's Gemini, Claude, or Local
        llm = self._router.get_text_model(TaskType.CONTENT_GENERATION)

        changes: list[ContentChange] = []

        for req in requests:
            prompt = self._build_prompt(req)

            llm_request = LlmRequest(
                prompt=prompt,
                system="You are an expert SEO and content strategist.",
                temperature=0.2,
            )

            try:
                # Ask the LLM to output according to our schema
                response = await llm.generate_structured(llm_request, GeneratedFix)

                change = ContentChange.suggest(
                    website_id=website_id,
                    tenant_id=tenant_id,
                    scan_id=scan_id,
                    page_url=req.page_url,
                    change_type=req.change_type,
                    priority=req.priority,
                    description=req.description,
                    before_value=req.current_value,
                    after_value=response.after_value,
                    ai_reasoning=response.ai_reasoning,
                )
                changes.append(change)

            except Exception as e:
                # Log error and skip this fix
                print(f"Failed to generate fix for {req.page_url} ({req.change_type}): {e}")

        return changes

    def _build_prompt(self, request: FixRequest) -> str:
        """Construct the prompt based on the type of fix needed."""

        base = f"Task: Fix {request.change_type.value} for URL: {request.page_url}\n"
        if request.current_value:
            base += f"Current Value: {request.current_value}\n"
        if request.context:
            base += f"Context: {request.context}\n"

        return base + "\nPlease generate the optimal replacement value."
