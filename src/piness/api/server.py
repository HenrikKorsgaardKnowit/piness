"""FastAPI application factory."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from piness.api.routes import create_router
from piness.store import EventBuffer, MessageBuffer

if TYPE_CHECKING:
    from piness.main import RefreshScheduler


def create_app(
    event_buffer: EventBuffer | None = None,
    message_buffer: MessageBuffer | None = None,
    refresh_scheduler: RefreshScheduler | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="piness", version="0.1.0")

    if event_buffer is None:
        event_buffer = EventBuffer(maxlen=100)
    if message_buffer is None:
        message_buffer = MessageBuffer(maxlen=50)

    app.state.event_buffer = event_buffer
    app.state.message_buffer = message_buffer
    app.state.refresh_scheduler = refresh_scheduler

    router = create_router()
    app.include_router(router)

    return app
