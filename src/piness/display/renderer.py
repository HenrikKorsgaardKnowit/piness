"""Composites panel images into a single display frame."""

from typing import Callable

from PIL import Image

from piness.display.driver import DisplayDriver


class Renderer:
    """Composites panel functions into a full-frame image and sends it to a driver.

    The display is divided into three horizontal bands:
      - Top third: system info
      - Middle third: graph
      - Bottom third: messages
    """

    WIDTH = 400
    HEIGHT = 300
    PANEL_HEIGHT = 100  # HEIGHT // 3

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

    def render(self) -> Image.Image:
        """Composite all panels and send the result to the driver."""
        frame = Image.new("RGB", (self.WIDTH, self.HEIGHT), "white")

        sysinfo_img = self.sysinfo_panel()
        graph_img = self.graph_panel()
        messages_img = self.messages_panel()

        frame.paste(sysinfo_img.crop((0, 0, self.WIDTH, self.PANEL_HEIGHT)), (0, 0))
        frame.paste(
            graph_img.crop((0, 0, self.WIDTH, self.PANEL_HEIGHT)),
            (0, self.PANEL_HEIGHT),
        )
        frame.paste(
            messages_img.crop((0, 0, self.WIDTH, self.PANEL_HEIGHT)),
            (0, self.PANEL_HEIGHT * 2),
        )

        self.driver.show(frame)
        return frame
