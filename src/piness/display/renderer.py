"""Composites panel images into a single display frame."""

from typing import Callable

from PIL import Image

from piness.display.driver import DisplayDriver


class Renderer:
    """Composites panel functions into a full-frame image and sends it to a driver.

    Layout:
      - Top: narrow sysinfo bar (400x36)
      - Middle: full-width data box (380x160)
      - Bottom: messages (380x88)
    """

    WIDTH = 400
    HEIGHT = 300

    def __init__(
        self,
        driver: DisplayDriver,
        sysinfo_panel: Callable[[], Image.Image],
        graph_panel: Callable[[], Image.Image],
        messages_panel: Callable[[], Image.Image],
    ) -> None:
        self.driver = driver
        self.sysinfo_panel = sysinfo_panel
        self.graph_panel = graph_panel
        self.messages_panel = messages_panel
        self._last_frame_bytes: bytes | None = None

    def render(self, force: bool = False) -> Image.Image:
        """Composite all panels. Only pushes to driver if frame changed or force=True."""
        frame = Image.new("RGB", (self.WIDTH, self.HEIGHT), "white")

        sysinfo_img = self.sysinfo_panel()
        graph_img = self.graph_panel()
        messages_img = self.messages_panel()

        # Header at top
        frame.paste(sysinfo_img, (0, 0))

        # Data box below header
        frame.paste(graph_img, (10, 44))

        # Messages row below data box
        frame.paste(messages_img, (10, 212))

        frame_bytes = frame.tobytes()
        if not force and frame_bytes == self._last_frame_bytes:
            return frame

        self._last_frame_bytes = frame_bytes
        self.driver.show(frame)
        return frame
