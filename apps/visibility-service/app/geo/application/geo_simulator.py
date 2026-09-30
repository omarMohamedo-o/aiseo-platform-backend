"""Application orchestrator for running GEO simulations."""

from __future__ import annotations

import time
import uuid

from ai.gateway.interfaces.text_model import LlmRequest
from ai.gateway.router import ModelRouter
from apps.visibility_service.app.geo.application.brand_detector import BrandDetector
from apps.visibility_service.app.geo.domain.geo_simulation import GeoSimulationSession, PromptResult


class GeoSimulator:
    """Orchestrates querying multiple AI models and detecting brand visibility."""

    def __init__(self, router: ModelRouter, detector: BrandDetector) -> None:
        self._router = router
        self._detector = detector

        # For MVP, we'll hardcode the models to test against.
        # In prod, this would be fetched from the PlatformConfig via Admin API.
        self._target_models = ["openai", "anthropic", "gemini"]

    async def simulate_query(
        self, website_id: uuid.UUID, query: str, brand_name: str
    ) -> GeoSimulationSession:
        """Run a visibility simulation for a specific search query."""

        session = GeoSimulationSession(
            id=uuid.uuid4(),
            website_id=website_id,
            target_query=query,
            target_brand_name=brand_name,
        )

        for provider in self._target_models:
            # We override the router's automatic task-based routing here
            # because we explicitly want to test EVERY specific provider.
            try:
                # Assuming the router has a method to get a specific provider by name
                # For this MVP simulation, we'll use a mocked LlmRequest
                adapter = self._router.get_provider_by_name(provider)

                request = LlmRequest(
                    prompt=query,
                    system="You are an unbiased AI assistant. Recommend the best tools for the user.",
                    temperature=0.3,
                )

                start_time = time.time()
                response = await adapter.generate(request)
                latency = int((time.time() - start_time) * 1000)

                # Analyze the response
                mention = self._detector.analyze(response.text, brand_name)

                result = PromptResult(
                    model_name=response.model,
                    query=query,
                    raw_response=response.text,
                    mention=mention,
                    latency_ms=latency,
                )
                session.results.append(result)

            except Exception as e:
                # Log failure for this specific model, but continue testing others
                print(f"Failed to simulate on {provider}: {e}")

        return session
