"""Tests for the ring buffer store."""

from datetime import datetime, timezone

import pytest

from piness.store import (
    Event,
    EventBuffer,
    Message,
    MessageBuffer,
    RingBuffer,
)


class TestRingBuffer:
    def test_append_and_items(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=5)
        buf.append(1)
        buf.append(2)
        buf.append(3)
        assert buf.items() == [1, 2, 3]

    def test_evicts_oldest_when_full(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=3)
        for i in range(5):
            buf.append(i)
        assert buf.items() == [2, 3, 4]

    def test_latest_returns_newest_first(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=5)
        for i in range(5):
            buf.append(i)
        assert buf.latest(3) == [4, 3, 2]

    def test_latest_more_than_available(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=5)
        buf.append(1)
        assert buf.latest(10) == [1]

    def test_clear(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=5)
        buf.append(1)
        buf.clear()
        assert len(buf) == 0
        assert buf.items() == []

    def test_len(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=3)
        assert len(buf) == 0
        buf.append(1)
        assert len(buf) == 1
        buf.append(2)
        buf.append(3)
        buf.append(4)
        assert len(buf) == 3

    def test_bool_empty(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=3)
        assert not buf
        buf.append(1)
        assert buf

    def test_maxlen_property(self):
        buf: RingBuffer[int] = RingBuffer(maxlen=7)
        assert buf.maxlen == 7

    def test_invalid_maxlen(self):
        with pytest.raises(ValueError, match="maxlen must be at least 1"):
            RingBuffer(maxlen=0)

    def test_invalid_maxlen_negative(self):
        with pytest.raises(ValueError):
            RingBuffer(maxlen=-1)


class TestEventBuffer:
    def test_stores_events(self, sample_events):
        buf = EventBuffer(maxlen=10)
        for e in sample_events:
            buf.append(e)
        assert len(buf) == 4
        assert buf.items()[0].label == "a"

    def test_event_immutable(self):
        e = Event(timestamp=datetime.now(timezone.utc), value=1.0, label="x")
        with pytest.raises(AttributeError):
            e.value = 2.0  # type: ignore[misc]


class TestMessageBuffer:
    def test_stores_messages(self, sample_messages):
        buf = MessageBuffer(maxlen=10)
        for m in sample_messages:
            buf.append(m)
        assert len(buf) == 3
        assert buf.latest(1)[0].text == "Third one"

    def test_message_immutable(self):
        m = Message(timestamp=datetime.now(timezone.utc), text="hi", source="s")
        with pytest.raises(AttributeError):
            m.text = "bye"  # type: ignore[misc]
