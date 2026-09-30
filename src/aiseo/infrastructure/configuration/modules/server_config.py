"""Configuration for FastAPI HTTP server and API Gateway."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """FastAPI application server settings."""

    host: str = Field(default="0.0.0.0", description="Bind host address")
    port: int = Field(default=8000, description="Bind port number")
    cors_origins: list[str] = Field(default_factory=lambda: ["*"], description="Allowed CORS origin domains")
    default_tenant: str = Field(default="default-tenant", description="Default tenant for unauthenticated requests")
    environment: str = Field(default="development", description="Runtime environment name")
    admin_username: str = Field(default="admin", description="Admin username")
    admin_password: str = Field(default="admin123", description="Admin password")
