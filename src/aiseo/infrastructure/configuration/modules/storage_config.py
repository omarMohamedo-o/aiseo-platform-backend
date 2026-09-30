"""Configuration for database, cache, and experiment registry."""
from __future__ import annotations

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """PostgreSQL database persistence configuration."""

    url: str = Field(
        default="postgresql+psycopg://aiseo:aiseo@localhost:5432/aiseo",
        description="SQLAlchemy async/sync connection URI",
    )
    pool_size: int = Field(default=10, description="Database connection pool size")


class RedisConfig(BaseModel):
    """Redis cache and Celery broker configuration."""

    url: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")


class MlflowConfig(BaseModel):
    """MLflow experiment tracking and model registry configuration."""

    tracking_uri: str = Field(default="sqlite:///mlflow.db", description="Tracking backend URI")
    registry_uri: str | None = Field(default=None, description="Model registry URI")
