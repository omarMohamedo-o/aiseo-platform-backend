"""FastAPI-level dependency wiring. Built once at app startup and reused."""

from __future__ import annotations

from fastapi import Request

from aiseo.application.websites.register_website import RegisterWebsiteService
from aiseo.infrastructure.configuration.composition_root import ApplicationContainer


def get_container(request: Request) -> ApplicationContainer:
    return request.app.state.container  # type: ignore[no-any-return]


def get_register_website_service(request: Request) -> RegisterWebsiteService:
    return get_container(request).register_website_service
