"""FastAPI application factory."""

from fastapi import FastAPI

from piness.api.routes import create_router
from piness.store import EventBuffer, MessageBuffer


def create_app(
    event_buffer: EventBuffer | None = None,
    message_buffer: MessageBuffer | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="piness", version="0.1.0")

    if event_buffer is None:
        event_buffer = EventBuffer(maxlen=100)
    if message_buffer is None:
        message_buffer = MessageBuffer(maxlen=50)

    app.state.event_buffer = event_buffer
    app.state.message_buffer = message_buffer

    router = create_router()
    app.include_router(router)

    return app
