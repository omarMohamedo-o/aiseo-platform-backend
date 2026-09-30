"""Unit tests for encrypted vault adapter."""
from __future__ import annotations

import pytest

from aiseo.infrastructure.security.vault import EncryptedVaultAdapter


def test_vault_seal_and_open() -> None:
    vault = EncryptedVaultAdapter(master_secret="test-secret-key-for-testing-12345")
    secret_text = "sk-proj-super-secret-api-key-12345678"

    sealed = vault.seal(secret_text)
    assert sealed != secret_text
    assert "." in sealed

    opened = vault.open(sealed)
    assert opened == secret_text


def test_vault_tamper_detection() -> None:
    vault = EncryptedVaultAdapter(master_secret="test-secret-key-for-testing-12345")
    sealed = vault.seal("sensitive-data")

    # Corrupt the ciphertext part
    parts = sealed.split(".")
    corrupted = parts[0] + "." + parts[1][:-2] + "AA"

    with pytest.raises(ValueError):
        vault.open(corrupted)


@pytest.mark.asyncio
async def test_vault_save_and_retrieve_credentials() -> None:
    vault = EncryptedVaultAdapter(master_secret="test-secret-key-for-testing-12345")
    tenant = "tenant-xyz"

    await vault.save_credentials(
        tenant_id=tenant,
        provider="openai",
        api_url="https://api.openai.com/v1",
        api_key="sk-real-openai-key",
        model="gpt-4o",
    )

    cred = await vault.get_credentials(tenant, "openai")
    assert cred is not None
    assert cred.provider == "openai"
    assert cred.api_url == "https://api.openai.com/v1"
    assert cred.api_key == "sk-real-openai-key"
    assert cred.model == "gpt-4o"

    await vault.delete_credentials(tenant, "openai")
    deleted = await vault.get_credentials(tenant, "openai")
    assert deleted is None
