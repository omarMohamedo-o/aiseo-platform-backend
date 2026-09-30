"""Email notification capability port."""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmailPort(Protocol):
    """Protocol for sending transactional and scheduled reports via email."""

    async def send_email(
        self,
        to: list[str],
        subject: str,
        html: str,
        text: str,
        from_sender: str | None = None,
    ) -> bool:
        """Send an email to recipients. Returns True on success, raises ProviderError on failure."""
        ...
