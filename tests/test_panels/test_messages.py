"""Tests for the messages panel."""

from datetime import datetime, timezone

from PIL import Image

from piness.display.panels.messages import render_messages, PANEL_WIDTH, PANEL_HEIGHT
from piness.store import Message


def _make_msg(text: str, source: str = "") -> Message:
    return Message(timestamp=datetime.now(timezone.utc), text=text, source=source)


class TestMessagesPanel:
    def test_returns_correct_size(self, sample_messages):
        img = render_messages(sample_messages)
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_empty_messages(self):
        img = render_messages([])
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_single_message(self):
        img = render_messages([_make_msg("hello", "bot")])
        assert isinstance(img, Image.Image)

    def test_long_message_truncated(self):
        long_text = "x" * 200
        img = render_messages([_make_msg(long_text)])
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_max_visible_limit(self):
        msgs = [_make_msg(f"msg {i}") for i in range(10)]
        img = render_messages(msgs)
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_returns_rgb(self, sample_messages):
        img = render_messages(sample_messages)
        assert img.mode == "RGB"
