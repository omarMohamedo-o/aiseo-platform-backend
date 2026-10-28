"""FastAPI-level dependency wiring. Built once at app startup and reused."""
from __future__ import annotations

from fastapi import Request

from aiseo.application.analysis.answer_analyzer import AnswerAnalyzerService
from aiseo.application.analysis.prompt_executor import PromptExecutorService
from aiseo.application.analysis.question_generator import QuestionGeneratorService
from aiseo.application.analysis.recommendation_generator import RecommendationGeneratorService
from aiseo.application.reporting.opportunity_scorer import OpportunityScorerService
from aiseo.application.reporting.report_generator import ReportGeneratorService
from aiseo.application.reporting.scheduled_reports import ScheduledReportsService
from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.infrastructure.configuration.composition_root import ApplicationContainer
from aiseo.ports.crawler.crawler_port import CrawlerPort
from aiseo.ports.evaluation.grounding_guard_port import GroundingGuardPort
from aiseo.ports.retrieval.reranker_port import RerankerPort
from aiseo.ports.cache.cache_port import CachePort
from aiseo.ports.evaluation.ground_truth_port import GroundTruthPort
from aiseo.ports.scraper.scraper_port import ScraperPort
from aiseo.ports.security.vault_port import VaultPort
from aiseo.ports.semantic.chunker_port import ChunkerPort
from aiseo.ports.trends.trends_port import TrendsPort


def get_container(request: Request) -> ApplicationContainer:
    return request.app.state.container  # type: ignore[no-any-return]


def get_crawler(request: Request) -> CrawlerPort:
    return get_container(request).crawler


def get_scraper(request: Request) -> ScraperPort:
    return get_container(request).scraper


def get_chunker(request: Request) -> ChunkerPort:
    return get_container(request).chunker


def get_register_website_service(request: Request) -> RegisterWebsiteService:
    return get_container(request).register_website_service


def get_question_generator_service(request: Request) -> QuestionGeneratorService:
    return get_container(request).question_generator


def get_recommendation_generator_service(request: Request) -> RecommendationGeneratorService:
    return get_container(request).recommendation_generator


def get_answer_analyzer_service(request: Request) -> AnswerAnalyzerService:
    return get_container(request).answer_analyzer


def get_grounding_guard(request: Request) -> GroundingGuardPort:
    return get_container(request).grounding_guard


def get_reranker(request: Request) -> RerankerPort:
    return get_container(request).reranker


def get_cache(request: Request) -> CachePort:
    return get_container(request).cache


def get_ground_truth_validator(request: Request) -> GroundTruthPort:
    return get_container(request).ground_truth_validator


def get_prompt_executor_service(request: Request) -> PromptExecutorService:
    return get_container(request).prompt_executor


def get_opportunity_scorer_service(request: Request) -> OpportunityScorerService:
    return get_container(request).opportunity_scorer


def get_report_generator_service(request: Request) -> ReportGeneratorService:
    return get_container(request).report_generator


def get_scheduled_reports_service(request: Request) -> ScheduledReportsService:
    return get_container(request).scheduled_reports


def get_trends_adapter(request: Request) -> TrendsPort:
    return get_container(request).trends_adapter


def get_vault(request: Request) -> VaultPort:
    return get_container(request).vault

def get_competitor_discovery_service(request: Request):
    return get_container(request).competitor_discovery
