"""Display driver abstraction for e-ink and mock output."""

import time
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

    def __init__(self, spi_delay: float = 0.01) -> None:
        if not HAS_INKY:
            raise RuntimeError(
                "inky library not available — install with pip install inky[rpi]"
            )
        self._display = inky_auto()
        self._patch_spi_delay(spi_delay)

    def _patch_spi_delay(self, delay: float) -> None:
        """Monkey-patch the inky driver to use a shorter SPI command delay.

        The stock jd79668 driver sleeps 300ms between every SPI command.
        With ~16 commands per refresh, that's ~4.8s of wasted time.
        """
        display = self._display

        def fast_send_command(command, data=None):
            from gpiod.line import Value
            display._gpio.set_value(display.cs_pin, Value.INACTIVE)
            display._gpio.set_value(display.dc_pin, Value.INACTIVE)
            time.sleep(delay)
            display._spi_bus.xfer3([command])
            if data is not None:
                display._gpio.set_value(display.dc_pin, Value.ACTIVE)
                display._spi_bus.xfer3(data)
            display._gpio.set_value(display.cs_pin, Value.ACTIVE)
            display._gpio.set_value(display.dc_pin, Value.INACTIVE)

        display._send_command = fast_send_command

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
