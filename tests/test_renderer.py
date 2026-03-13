"""Tests for the display renderer."""

from PIL import Image

from piness.display.renderer import Renderer


class TestRenderer:
    def test_composites_three_panels(self, mock_driver):
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: Image.new("RGB", (400, 36), "red"),
            graph_panel=lambda: Image.new("RGB", (380, 160), "green"),
            messages_panel=lambda: Image.new("RGB", (380, 88), "blue"),
        )
        frame = renderer.render(force=True)
        assert frame.size == (400, 300)

        # Header area is red
        assert frame.getpixel((200, 10)) == (255, 0, 0)
        # Graph area is green (pasted at x=10, y=44)
        assert frame.getpixel((200, 120)) == (0, 128, 0)
        # Messages area is blue (pasted at x=10, y=212)
        assert frame.getpixel((200, 250)) == (0, 0, 255)

    def test_saves_to_driver(self, mock_driver, tmp_path):
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: Image.new("RGB", (400, 36), "white"),
            graph_panel=lambda: Image.new("RGB", (380, 160), "white"),
            messages_panel=lambda: Image.new("RGB", (380, 88), "white"),
        )
        renderer.render(force=True)
        saved = Image.open(mock_driver.output_path)
        assert saved.size == (400, 300)

    def test_skips_refresh_when_frame_unchanged(self, mock_driver):
        call_count = 0
        original_show = mock_driver.show

        def counting_show(image):
            nonlocal call_count
            call_count += 1
            original_show(image)

        mock_driver.show = counting_show

        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: Image.new("RGB", (400, 36), "white"),
            graph_panel=lambda: Image.new("RGB", (380, 160), "white"),
            messages_panel=lambda: Image.new("RGB", (380, 88), "white"),
        )
        renderer.render(force=True)
        assert call_count == 1

        # Second render with same content should skip
        renderer.render()
        assert call_count == 1

    def test_refreshes_when_frame_changes(self, mock_driver):
        call_count = 0
        original_show = mock_driver.show

        def counting_show(image):
            nonlocal call_count
            call_count += 1
            original_show(image)

        mock_driver.show = counting_show

        color = ["white"]
        renderer = Renderer(
            driver=mock_driver,
            sysinfo_panel=lambda: Image.new("RGB", (400, 36), color[0]),
            graph_panel=lambda: Image.new("RGB", (380, 160), "white"),
            messages_panel=lambda: Image.new("RGB", (380, 88), "white"),
        )
        renderer.render(force=True)
        assert call_count == 1

        # Change the content
        color[0] = "black"
        renderer.render()
        assert call_count == 2
