"""Graph panel rendering a bar chart from event data."""

from PIL import Image, ImageDraw, ImageFont

from piness.store import Event

PANEL_WIDTH = 380
PANEL_HEIGHT = 160
MARGIN = 8
BAR_GAP = 2


def render_graph(events: list[Event]) -> Image.Image:
    """Return a full-width Pillow Image with a thin border and bar chart inside."""
    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    # Thin border
    draw.rectangle([0, 0, PANEL_WIDTH - 1, PANEL_HEIGHT - 1], outline="black", width=1)

    if not events:
        draw.text((MARGIN, PANEL_HEIGHT // 2 - 8), "no data", fill="black", font=font)
        return img

    max_val = max(e.value for e in events)
    if max_val == 0:
        max_val = 1.0

    usable_w = PANEL_WIDTH - 2 * MARGIN
    usable_h = PANEL_HEIGHT - 2 * MARGIN
    bar_width = max(1, (usable_w - BAR_GAP * len(events)) // len(events))

    for i, event in enumerate(events):
        bar_height = int((event.value / max_val) * usable_h)
        x0 = MARGIN + i * (bar_width + BAR_GAP)
        y0 = MARGIN + usable_h - bar_height
        x1 = x0 + bar_width
        y1 = MARGIN + usable_h
        draw.rectangle([x0, y0, x1, y1], fill="black")

    return img
