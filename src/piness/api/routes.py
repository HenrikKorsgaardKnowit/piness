"""API route definitions for event and message ingestion."""

from datetime import datetime, timezone

from fastapi import APIRouter, Request
from pydantic import BaseModel

from piness.store import Event, EventBuffer, Message, MessageBuffer


class EventIn(BaseModel):
    value: float
    label: str = ""


class MessageIn(BaseModel):
    text: str
    source: str = ""


def create_router() -> APIRouter:
    router = APIRouter()

    def _notify_refresh(request: Request) -> None:
        scheduler = getattr(request.app.state, "refresh_scheduler", None)
        if scheduler is not None:
            scheduler.notify()

    @router.post("/events", status_code=201)
    async def post_event(body: EventIn, request: Request) -> dict:
        buf: EventBuffer = request.app.state.event_buffer
        event = Event(
            timestamp=datetime.now(timezone.utc),
            value=body.value,
            label=body.label,
        )
        buf.append(event)
        _notify_refresh(request)
        return {"status": "ok", "events_count": len(buf)}

    @router.post("/messages", status_code=201)
    async def post_message(body: MessageIn, request: Request) -> dict:
        buf: MessageBuffer = request.app.state.message_buffer
        message = Message(
            timestamp=datetime.now(timezone.utc),
            text=body.text,
            source=body.source,
        )
        buf.append(message)
        _notify_refresh(request)
        return {"status": "ok", "messages_count": len(buf)}

    @router.get("/status")
    async def get_status(request: Request) -> dict:
        event_buf: EventBuffer = request.app.state.event_buffer
        message_buf: MessageBuffer = request.app.state.message_buffer
        return {
            "status": "ok",
            "events_count": len(event_buf),
            "messages_count": len(message_buf),
        }

    return router
