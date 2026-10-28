"""Port interface for enterprise webhook incident alerting.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class WebhookAlert:
    """Incident payload for enterprise operations & monitoring."""
    domain: str
    alert_type: str
    severity: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class WebhookAlertPort(abc.ABC):
    """Abstract port for dispatching enterprise alerting webhooks."""

    @abc.abstractmethod
    async def send_alert(self, alert: WebhookAlert) -> bool:
        """Dispatches an alert to configured downstream webhooks."""
        raise NotImplementedError

