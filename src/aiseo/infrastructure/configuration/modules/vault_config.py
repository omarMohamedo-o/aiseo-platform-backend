"""Configuration for tenant security vault and cryptographic keys."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VaultConfig(BaseModel):
    """Encrypted Vault adapter configuration."""

    master_secret: str = Field(
        default="aiseo-default-master-secret-key-change-in-production-12345",
        description="Master encryption key used for PBKDF2/AES-256-GCM derivation",
    )
    algorithm: str = Field(default="AES-256-GCM", description="Authenticated cipher algorithm")
    salt: str = Field(default="aiseo-vault-salt", description="Salt used for HKDF key derivation")
