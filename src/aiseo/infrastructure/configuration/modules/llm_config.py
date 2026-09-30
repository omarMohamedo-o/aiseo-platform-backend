"""Configuration for Multi-LLM providers and prompt generation."""
from __future__ import annotations

from pydantic import BaseModel, Field


class LlmConfig(BaseModel):
    """Large Language Model provider settings."""

    provider: str = Field(default="openai", description="Default active LLM provider")
    model: str = Field(default="gpt-4o-mini", description="Default model identifier")
    temperature: float = Field(default=0.0, description="Sampling temperature")
    api_key: str | None = Field(default=None, description="Generic fallback API key")
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API key")
    claude_api_key: str | None = Field(default=None, description="Anthropic Claude API key")
    perplexity_api_key: str | None = Field(default=None, description="Perplexity API key")
