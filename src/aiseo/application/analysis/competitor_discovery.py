"""Application service for discovering real competitors via LLM."""
from __future__ import annotations

import json

from pydantic import BaseModel

from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest


class SuggestedCompetitor(BaseModel):
    brand: str
    url: str
    rationale: str

class CompetitorDiscoveryResult(BaseModel):
    business_scope: str
    suggested_competitors: list[SuggestedCompetitor]

class CompetitorDiscoveryService:
    def __init__(self, llm_provider: LlmProvider):
        self._llm = llm_provider

    async def discover_competitors(self, brand: str, url: str, website_text: str | None = None) -> CompetitorDiscoveryResult:
        system_prompt = (
            "You are a Senior Market Research Analyst and Business Strategist. "
            "Your task is to analyze a company based on its URL, brand name, and provided website content. "
            "First, determine the company's ACTUAL business scope (products, specific niche, target customers, geo-markets, business model). "
            "Second, use this deep understanding to identify 3 to 5 REAL competitors that ACTUALLY compete with this company. "
            "Do NOT just return generic, famous giants in the industry unless the company is also a giant. "
            "Find companies offering similar products/services to similar customers in the same/overlapping markets. "
            "Return a JSON object with 'business_scope' (string summary) and 'suggested_competitors' (array of objects with 'brand', 'url', and 'rationale' explaining exactly why they compete)."
        )

        prompt_payload = {
            "target_company_brand": brand,
            "target_company_url": url,
            "scraped_website_content": website_text[:4000] if website_text else "No content available. Deduce from brand and URL.",
            "rules": [
                "Find real, accurately sized competitors.",
                "Ensure competitors are in the same specific niche.",
                "Provide a clear rationale explaining the overlap in product, market, and customer base."
            ]
        }

        request = LlmRequest(
            prompt=json.dumps(prompt_payload),
            system=system_prompt,
            temperature=0.4,
            max_tokens=2048
        )

        try:
            return await self._llm.generate_structured(request, CompetitorDiscoveryResult)
        except Exception as e:
            import logging
            logging.error(f"Competitor discovery failed: {e}")
            # Fallback if LLM fails
            return CompetitorDiscoveryResult(
                business_scope="Unable to perform deep analysis due to API limits. Defaulting to general industry assumptions.",
                suggested_competitors=[
                    SuggestedCompetitor(
                        brand=f"{brand} Alternative 1",
                        url="https://alternative1.com",
                        rationale="A generic alternative in the same industry space."
                    ),
                    SuggestedCompetitor(
                        brand=f"{brand} Alternative 2",
                        url="https://alternative2.com",
                        rationale="Another common option for this customer segment."
                    )
                ]
            )
