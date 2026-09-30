"""Configuration-driven settings. Domain/application code never reads env vars directly."""

from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LlmConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.0


class EmbeddingConfig(BaseModel):
    provider: str = "openai"
    model: str = "text-embedding-3-small"
    dimensions: int = 1536


class ClusteringConfig(BaseModel):
    algorithm: str = "hdbscan"
    min_cluster_size: int = 5


class ScoringConfig(BaseModel):
    seo_version: str = "seo-v1"
    aeo_version: str = "aeo-v1"
    geo_version: str = "geo-v1"


class MlflowConfig(BaseModel):
    tracking_uri: str = "sqlite:///mlflow.db"
    registry_uri: str | None = None


class DatabaseConfig(BaseModel):
    url: str = "postgresql+psycopg://aiseo:aiseo@localhost:5432/aiseo"
    pool_size: int = 10


class RedisConfig(BaseModel):
    url: str = "redis://localhost:6379/0"


class Settings(BaseSettings):
    """Root, immutable, configuration-driven settings object.

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

    llm: LlmConfig = Field(default_factory=LlmConfig)
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    clustering: ClusteringConfig = Field(default_factory=ClusteringConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    mlflow: MlflowConfig = Field(default_factory=MlflowConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)


def load_settings() -> Settings:
    """Single entry point for settings construction (composition root only)."""
    return Settings()
