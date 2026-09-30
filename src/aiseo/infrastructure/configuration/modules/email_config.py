"""Configuration for notification bus and email reporting delivery."""
from __future__ import annotations

from pydantic import BaseModel, Field


class EmailConfig(BaseModel):
    """Email delivery adapter configuration (Resend)."""

    api_url: str = Field(default="https://api.resend.com/emails", description="Resend REST API endpoint")
    api_key: str | None = Field(default=None, description="Resend API Key")
    default_from_email: str = Field(
        default="reports@aiseo-platform.io",
        description="Default sender email address",
    )
    timeout_seconds: float = Field(default=10.0, description="HTTP delivery timeout in seconds")
