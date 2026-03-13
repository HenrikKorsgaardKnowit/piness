"""System info panel showing hostname and IP address."""

import socket

from PIL import Image, ImageDraw, ImageFont

PANEL_WIDTH = 400
PANEL_HEIGHT = 36


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
    """Return a Pillow Image with hostname and IP on one line."""
    hostname = hostname if hostname is not None else get_hostname()
    ip_address = ip_address if ip_address is not None else get_ip_address()

    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()

    # Hostname left-aligned
    draw.text((10, 4), hostname, fill="black", font=font)

    # IP right-aligned
    ip_bbox = draw.textbbox((0, 0), ip_address, font=font)
    ip_width = ip_bbox[2] - ip_bbox[0]
    draw.text((PANEL_WIDTH - 10 - ip_width, 4), ip_address, fill="black", font=font)

    # Divider line at bottom
    draw.line([(10, PANEL_HEIGHT - 1), (PANEL_WIDTH - 10, PANEL_HEIGHT - 1)], fill="black", width=1)

    return img
