"""Display driver abstraction for e-ink and mock output."""

from abc import ABC, abstractmethod
from PIL import Image

try:
    from inky.auto import auto as inky_auto

    HAS_INKY = True
except ImportError:
    HAS_INKY = False


class DisplayDriver(ABC):
    """Abstract base class for display drivers."""

    @abstractmethod
    def show(self, image: Image.Image) -> None:
        """Display an image on the screen."""

    @abstractmethod
    def clear(self) -> None:
        """Clear the display."""


class InkyDriver(DisplayDriver):
    """Driver that renders to an InkyWHAT e-ink display."""

    def __init__(self) -> None:
        if not HAS_INKY:
            raise RuntimeError(
                "inky library not available — install with pip install inky[rpi]"
            )
        self._display = inky_auto()

    def show(self, image: Image.Image) -> None:
        self._display.set_image(image)
        self._display.show()

    def clear(self) -> None:
        blank = Image.new("P", (self._display.WIDTH, self._display.HEIGHT), 0)
        self._display.set_image(blank)
        self._display.show()


class MockDriver(DisplayDriver):
    """Driver that saves the image to a file for local development."""

    OUTPUT_PATH = "/tmp/piness_display.png"

    def __init__(self, output_path: str | None = None) -> None:
        self.output_path = output_path or self.OUTPUT_PATH

    def show(self, image: Image.Image) -> None:
        image.save(self.output_path)

    def clear(self) -> None:
        blank = Image.new("RGB", (400, 300), "white")
        blank.save(self.output_path)
