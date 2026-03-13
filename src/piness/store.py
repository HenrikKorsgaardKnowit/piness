"""Ring buffers for event and message storage."""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Event:
    """A timestamped numeric event."""

    timestamp: datetime
    value: float
    label: str = ""


@dataclass(frozen=True)
class Message:
    """A timestamped text message."""

    timestamp: datetime
    text: str
    source: str = ""


class RingBuffer(Generic[T]):
    """Fixed-size FIFO buffer backed by collections.deque."""

    def __init__(self, maxlen: int) -> None:
        if maxlen < 1:
            raise ValueError("maxlen must be at least 1")
        self._buf: deque[T] = deque(maxlen=maxlen)

    def append(self, item: T) -> None:
        """Add an item, evicting the oldest if full."""
        self._buf.append(item)

    def items(self) -> list[T]:
        """Return all items oldest-first."""
        return list(self._buf)

    def latest(self, n: int = 1) -> list[T]:
        """Return the n most recent items, newest-first."""
        return list(reversed(list(self._buf)))[:n]

    def clear(self) -> None:
        """Remove all items."""
        self._buf.clear()

    @property
    def maxlen(self) -> int:
        return self._buf.maxlen  # type: ignore[return-value]

    def __len__(self) -> int:
        return len(self._buf)

    def __bool__(self) -> bool:
        return len(self._buf) > 0


class EventBuffer(RingBuffer[Event]):
    """Ring buffer typed for Event items."""

    pass


class MessageBuffer(RingBuffer[Message]):
    """Ring buffer typed for Message items."""

    pass
