"""Shared test fixtures."""

from datetime import datetime, timezone

import pytest

from piness.display.driver import MockDriver
from piness.store import Event, EventBuffer, Message, MessageBuffer


@pytest.fixture
def mock_driver(tmp_path):
    """A MockDriver that writes to a temporary directory."""
    return MockDriver(output_path=str(tmp_path / "display.png"))


@pytest.fixture
def sample_events() -> list[Event]:
    """A list of sample events for testing."""
    base = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return [
        Event(timestamp=base, value=10.0, label="a"),
        Event(timestamp=base, value=25.0, label="b"),
        Event(timestamp=base, value=5.0, label="c"),
        Event(timestamp=base, value=40.0, label="d"),
    ]


@pytest.fixture
def sample_messages() -> list[Message]:
    """A list of sample messages for testing."""
    base = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return [
        Message(timestamp=base, text="Hello world", source="test"),
        Message(timestamp=base, text="Second message", source="bot"),
        Message(timestamp=base, text="Third one", source=""),
    ]


@pytest.fixture
def event_buffer(sample_events) -> EventBuffer:
    buf = EventBuffer(maxlen=10)
    for e in sample_events:
        buf.append(e)
    return buf


@pytest.fixture
def message_buffer(sample_messages) -> MessageBuffer:
    buf = MessageBuffer(maxlen=10)
    for m in sample_messages:
        buf.append(m)
    return buf
