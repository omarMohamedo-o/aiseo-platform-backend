"""Encrypted credentials vault adapter using AES-256-GCM."""
from __future__ import annotations

import base64
import hashlib
import json
import os
from datetime import UTC, datetime

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from aiseo.ports.security.vault_port import StoredCredential, VaultPort


class EncryptedVaultAdapter(VaultPort):
    """Secure encrypted storage for tenant/workspace integration credentials.

    Uses AES-256-GCM authenticated encryption. An in-memory store is maintained here,
    with database table persistence wired at the repository layer.
    """

    def __init__(self, master_secret: str | None = None) -> None:
        secret = master_secret or os.getenv("AISEO_SECURITY__SECRET_KEY") or "default-insecure-dev-secret-key-32b"
        # Derive 32-byte key via SHA-256
        self._key = hashlib.sha256(secret.encode("utf-8")).digest()
        self._aesgcm = AESGCM(self._key)
        # In-memory backing store for tenant credentials: (tenant_id, provider) -> encrypted record
        self._store: dict[tuple[str, str], dict[str, str]] = {}

    def seal(self, plaintext: str) -> str:
        """Encrypt plaintext using AES-256-GCM with a randomized 12-byte nonce."""
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        # Store as base64url(nonce).base64url(ciphertext)
        b64_nonce = base64.urlsafe_b64encode(nonce).decode("ascii")
        b64_cipher = base64.urlsafe_b64encode(ciphertext).decode("ascii")
        return f"{b64_nonce}.{b64_cipher}"

    def open(self, sealed_token: str) -> str:
        """Decrypt sealed AES-256-GCM token."""
        parts = sealed_token.split(".")
        if len(parts) != 2:
            raise ValueError("Malformed encrypted token format")

        nonce = base64.urlsafe_b64decode(parts[0].encode("ascii"))
        ciphertext = base64.urlsafe_b64decode(parts[1].encode("ascii"))

        try:
            decrypted_bytes = self._aesgcm.decrypt(nonce, ciphertext, None)
        except InvalidTag as exc:
            raise ValueError("Tampered or invalid ciphertext authentication tag") from exc
        return decrypted_bytes.decode("utf-8")

    async def save_credentials(
        self,
        tenant_id: str,
        provider: str,
        api_url: str,
        api_key: str,
        model: str = "",
    ) -> None:
        now_str = datetime.now(UTC).isoformat()
        payload = json.dumps({"apiKey": api_key, "model": model})

        self._store[(tenant_id, provider)] = {
            "encryptedApiUrl": self.seal(api_url),
            "encryptedApiKey": self.seal(payload),
            "updatedAt": now_str,
        }

    async def get_credentials(
        self, tenant_id: str, provider: str
    ) -> StoredCredential | None:
        rec = self._store.get((tenant_id, provider))
        if not rec:
            return None

        api_url = self.open(rec["encryptedApiUrl"])
        raw_key_payload = self.open(rec["encryptedApiKey"])

        try:
            parsed = json.loads(raw_key_payload)
            api_key = parsed.get("apiKey", "")
            model = parsed.get("model", "")
        except json.JSONDecodeError:
            api_key = raw_key_payload
            model = ""

        return StoredCredential(
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            model=model,
            updated_at=rec.get("updatedAt"),
        )

    async def delete_credentials(self, tenant_id: str, provider: str) -> None:
        self._store.pop((tenant_id, provider), None)
