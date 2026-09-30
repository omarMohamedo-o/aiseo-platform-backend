"""Configuration-driven settings composed from separated, modular configuration models."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiseo.infrastructure.configuration.modules.crawler_config import CrawlerConfig, ExtractorConfig
from aiseo.infrastructure.configuration.modules.email_config import EmailConfig
from aiseo.infrastructure.configuration.modules.llm_config import LlmConfig
from aiseo.infrastructure.configuration.modules.opportunity_config import (
    OpportunityScorerConfig,
    ScoringConfig,
)
from aiseo.infrastructure.configuration.modules.resilience_config import ResilienceConfig
from aiseo.infrastructure.configuration.modules.semantic_config import (
    ChunkerConfig,
    ClusteringConfig,
    EmbeddingConfig,
)
from aiseo.infrastructure.configuration.modules.server_config import ServerConfig
from aiseo.infrastructure.configuration.modules.storage_config import (
    DatabaseConfig,
    MlflowConfig,
    RedisConfig,
)
from aiseo.infrastructure.configuration.modules.trends_config import TrendsConfig
from aiseo.infrastructure.configuration.modules.vault_config import VaultConfig

# Re-export individual configs for direct modular consumption across the application
__all__ = [
    "ChunkerConfig",
    "ClusteringConfig",
    "CrawlerConfig",
    "DatabaseConfig",
    "EmailConfig",
    "EmbeddingConfig",
    "ExtractorConfig",
    "LlmConfig",
    "MlflowConfig",
    "OpportunityScorerConfig",
    "RedisConfig",
    "ResilienceConfig",
    "ScoringConfig",
    "ServerConfig",
    "Settings",
    "TrendsConfig",
    "VaultConfig",
    "load_settings",
]


class Settings(BaseSettings):
    """Root, immutable, configuration-driven settings object.

    Composed from dedicated, decoupled configuration modules.
    Populated from environment variables / .env at process start, in the
    composition root only. Nothing below `infrastructure` should construct
    this directly.
    """

    model_config = SettingsConfigDict(
        env_prefix="AISEO_",
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    environment: str = "development"

    # Separated Modular Configurations
    server: ServerConfig = Field(default_factory=ServerConfig)
    llm: LlmConfig = Field(default_factory=LlmConfig)
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    chunker: ChunkerConfig = Field(default_factory=ChunkerConfig)
    clustering: ClusteringConfig = Field(default_factory=ClusteringConfig)
    crawler: CrawlerConfig = Field(default_factory=CrawlerConfig)
    extractor: ExtractorConfig = Field(default_factory=ExtractorConfig)
    vault: VaultConfig = Field(default_factory=VaultConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)
    trends: TrendsConfig = Field(default_factory=TrendsConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    resilience: ResilienceConfig = Field(default_factory=ResilienceConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    mlflow: MlflowConfig = Field(default_factory=MlflowConfig)


def load_settings() -> Settings:
    """Single entry point for settings construction (composition root only)."""
    return Settings()
