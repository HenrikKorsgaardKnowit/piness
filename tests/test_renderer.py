"""Tests for the display renderer."""

from PIL import Image

from piness.display.renderer import Renderer


def _make_panel(color: str) -> Image.Image:
    return Image.new("RGB", (400, 100), color)


class TestRenderer:
    def test_composites_three_panels(self, mock_driver):
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: _make_panel("red"),
            graph_panel=lambda: _make_panel("green"),
            messages_panel=lambda: _make_panel("blue"),
        )
        frame = renderer.render()
        assert frame.size == (400, 300)

        # Check that each third has the expected color
        assert frame.getpixel((200, 50)) == (255, 0, 0)  # red top
        assert frame.getpixel((200, 150)) == (0, 128, 0)  # green middle
        assert frame.getpixel((200, 250)) == (0, 0, 255)  # blue bottom

    def test_saves_to_driver(self, mock_driver, tmp_path):
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: _make_panel("white"),
            graph_panel=lambda: _make_panel("white"),
            messages_panel=lambda: _make_panel("white"),
        )
        renderer.render()
        # MockDriver should have saved the file
        saved = Image.open(mock_driver.output_path)
        assert saved.size == (400, 300)

    def test_handles_oversized_panels(self, mock_driver):
        """Panels larger than expected are cropped."""
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: Image.new("RGB", (500, 200), "red"),
            graph_panel=lambda: Image.new("RGB", (400, 100), "green"),
            messages_panel=lambda: Image.new("RGB", (400, 100), "blue"),
        )
        frame = renderer.render()
        assert frame.size == (400, 300)
