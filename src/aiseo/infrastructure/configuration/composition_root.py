"""Composition root: reads configuration, resolves providers/algorithms,
builds adapters, and wires application services. This is the ONLY module
allowed to instantiate concrete infrastructure classes directly."""
from __future__ import annotations

from dataclasses import dataclass

from aiseo.adapters.crawler.httpx_crawler import HttpxCrawler
from aiseo.adapters.llm.gemini_provider import GeminiProvider
from aiseo.adapters.llm.openai_provider import OpenAiProvider
from aiseo.adapters.notifications.resend_email_adapter import ResendEmailAdapter
from aiseo.adapters.persistence.in_memory_website_repository import InMemoryWebsiteRepository
from aiseo.adapters.scraper.trafilatura_scraper import TrafilaturaScraper
from aiseo.adapters.semantic.in_memory_vector_store import InMemoryVectorStore
from aiseo.adapters.semantic.recursive_chunker import RecursiveChunker
from aiseo.adapters.trends.multi_trends_adapter import MultiTrendsAdapter
from aiseo.application.analysis.answer_analyzer import AnswerAnalyzerService
from aiseo.application.analysis.prompt_executor import PromptExecutorService
from aiseo.application.analysis.question_generator import QuestionGeneratorService
from aiseo.application.analysis.recommendation_generator import RecommendationGeneratorService
from aiseo.application.rag.prompt_builder import RagPromptBuilder
from aiseo.application.reporting.opportunity_scorer import OpportunityScorerService
from aiseo.application.reporting.report_generator import ReportGeneratorService
from aiseo.application.reporting.scheduled_reports import ScheduledReportsService
from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.infrastructure.configuration.registry import Registry
from aiseo.infrastructure.configuration.settings import Settings, load_settings
from aiseo.infrastructure.security.vault import EncryptedVaultAdapter
from aiseo.ports.clustering.clustering_algorithm import ClusteringAlgorithm
from aiseo.ports.crawler.crawler_port import CrawlerPort
from aiseo.ports.llm.llm_provider import LlmProvider
from aiseo.ports.notifications.email_port import EmailPort
from aiseo.ports.persistence.website_repository import WebsiteRepository
from aiseo.ports.scraper.scraper_port import ScraperPort
from aiseo.ports.security.vault_port import VaultPort
from aiseo.ports.semantic.chunker_port import ChunkerPort
from aiseo.ports.semantic.vector_store_port import VectorStorePort
from aiseo.ports.trends.trends_port import TrendsPort


@dataclass(frozen=True)
class ApplicationContainer:
    """Holds fully-wired application services for the process lifetime."""

    settings: Settings
    website_repository: WebsiteRepository
    register_website_service: RegisterWebsiteService
    clustering_registry: Registry[ClusteringAlgorithm]
    llm_registry: Registry[LlmProvider]
    chunker: ChunkerPort
    vector_store: VectorStorePort
    prompt_builder: RagPromptBuilder

    # Crawling & Scraping capabilities
    crawler: CrawlerPort
    scraper: ScraperPort

    # Command Center capabilities
    vault: VaultPort
    email_adapter: EmailPort
    trends_adapter: TrendsPort
    question_generator: QuestionGeneratorService
    recommendation_generator: RecommendationGeneratorService
    answer_analyzer: AnswerAnalyzerService
    prompt_executor: PromptExecutorService
    opportunity_scorer: OpportunityScorerService
    report_generator: ReportGeneratorService
    scheduled_reports: ScheduledReportsService
    
    from aiseo.application.analysis.competitor_discovery import CompetitorDiscoveryService
    competitor_discovery: CompetitorDiscoveryService


def _build_clustering_registry() -> Registry[ClusteringAlgorithm]:
    registry: Registry[ClusteringAlgorithm] = Registry()
    return registry


def _build_llm_registry(settings: Settings) -> Registry[LlmProvider]:
    registry: Registry[LlmProvider] = Registry()

    openai_key = settings.llm.openai_api_key or settings.llm.api_key or ""
    gemini_key = settings.llm.gemini_api_key or settings.llm.api_key or ""

    registry.register(
        "openai",
        lambda: OpenAiProvider(
            api_key=openai_key,
            default_model=settings.llm.model,
        ),
    )
    registry.register(
        "gemini",
        lambda: GeminiProvider(
            api_key=gemini_key,
            default_model=settings.llm.model,
        ),
    )
    return registry


def build_container(settings: Settings | None = None) -> ApplicationContainer:
    """Build the application container from configuration.

    Domain and application services never call this function or read
    settings themselves -- they only receive already-constructed
    dependencies through their constructors.
    """
    resolved_settings = settings or load_settings()

    website_repository: WebsiteRepository = InMemoryWebsiteRepository()
    register_website_service = RegisterWebsiteService(website_repository=website_repository)
    llm_registry = _build_llm_registry(resolved_settings)

    # Resolve default LLM provider if configured
    default_llm: LlmProvider | None = None
    try:
        default_llm = llm_registry.resolve(resolved_settings.llm.provider)
    except Exception:
        default_llm = None

    vault: VaultPort = EncryptedVaultAdapter(
        master_secret=resolved_settings.vault.master_secret
    )
    email_adapter: EmailPort = ResendEmailAdapter(
        api_key=resolved_settings.email.api_key or resolved_settings.llm.api_key or "mock-resend-key",
        api_url=resolved_settings.email.api_url,
    )
    trends_adapter: TrendsPort = MultiTrendsAdapter()

    question_generator = QuestionGeneratorService(
        llm_provider=default_llm or OpenAiProvider(api_key="mock-key")
    )
    recommendation_generator = RecommendationGeneratorService(
        llm_provider=default_llm or OpenAiProvider(api_key="mock-key")
    )
    answer_analyzer = AnswerAnalyzerService(llm_provider=default_llm)
    prompt_executor = PromptExecutorService(llm_registry=llm_registry)
    opportunity_scorer = OpportunityScorerService(
        config=resolved_settings.scoring.opportunity
    )
    report_generator = ReportGeneratorService(llm_provider=default_llm)
    scheduled_reports = ScheduledReportsService(
        email_adapter=email_adapter,
        report_generator=report_generator,
        opportunity_scorer=opportunity_scorer,
    )
    from aiseo.application.analysis.competitor_discovery import CompetitorDiscoveryService
    competitor_discovery = CompetitorDiscoveryService(llm_provider=default_llm or OpenAiProvider(api_key="mock-key"))

    crawler = HttpxCrawler(timeout=resolved_settings.crawler.timeout_seconds)
    scraper = TrafilaturaScraper(timeout=resolved_settings.extractor.timeout_seconds)

    return ApplicationContainer(
        settings=resolved_settings,
        website_repository=website_repository,
        register_website_service=register_website_service,
        clustering_registry=_build_clustering_registry(),
        llm_registry=llm_registry,
        chunker=RecursiveChunker(
            separators=resolved_settings.chunker.separators,
        ),
        vector_store=InMemoryVectorStore(),
        prompt_builder=RagPromptBuilder(),
        crawler=crawler,
        scraper=scraper,
        vault=vault,
        email_adapter=email_adapter,
        trends_adapter=trends_adapter,
        question_generator=question_generator,
        recommendation_generator=recommendation_generator,
        answer_analyzer=answer_analyzer,
        prompt_executor=prompt_executor,
        opportunity_scorer=opportunity_scorer,
        report_generator=report_generator,
        scheduled_reports=scheduled_reports,
        competitor_discovery=competitor_discovery,
    )
