"""Tests for the graph panel."""

from datetime import datetime, timezone

from PIL import Image

from piness.display.panels.graph import render_graph, PANEL_WIDTH, PANEL_HEIGHT
from piness.store import Event


def _make_event(value: float, label: str = "") -> Event:
    return Event(timestamp=datetime.now(timezone.utc), value=value, label=label)


class TestGraphPanel:
    def test_returns_correct_size(self, sample_events):
        img = render_graph(sample_events)
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_empty_events(self):
        img = render_graph([])
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_single_event(self):
        img = render_graph([_make_event(100)])
        assert isinstance(img, Image.Image)

    def test_all_zero_values(self):
        events = [_make_event(0) for _ in range(5)]
        img = render_graph(events)
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_many_events(self):
        events = [_make_event(float(i)) for i in range(50)]
        img = render_graph(events)
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_returns_rgb(self, sample_events):
        img = render_graph(sample_events)
        assert img.mode == "RGB"
