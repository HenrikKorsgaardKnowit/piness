"""System info panel showing hostname and IP address."""

import socket

from PIL import Image, ImageDraw, ImageFont

PANEL_WIDTH = 400
PANEL_HEIGHT = 100


def get_hostname() -> str:
    """Return the system hostname."""
    return socket.gethostname()


def get_ip_address() -> str:
    """Return the primary IP address, or a fallback string."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "no network"


def render_sysinfo(
    hostname: str | None = None, ip_address: str | None = None
) -> Image.Image:
    """Return a Pillow Image with hostname and IP address."""
    hostname = hostname if hostname is not None else get_hostname()
    ip_address = ip_address if ip_address is not None else get_ip_address()

    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()

    draw.text((10, 10), f"Host: {hostname}", fill="black", font=font)
    draw.text((10, 40), f"IP:   {ip_address}", fill="black", font=font)

    return img
