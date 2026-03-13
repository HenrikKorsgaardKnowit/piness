"""Graph panel rendering a bar chart from event data."""

from PIL import Image, ImageDraw, ImageFont

from piness.store import Event

PANEL_WIDTH = 400
PANEL_HEIGHT = 100
MARGIN = 10
BAR_GAP = 2


def render_graph(events: list[Event]) -> Image.Image:
    """Return a Pillow Image with a bar chart of event values.

    Bars are scaled relative to the maximum value in the list.
    An empty event list produces a blank panel with a "no data" label.
    """
    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    if not events:
        draw.text((MARGIN, PANEL_HEIGHT // 2 - 8), "no data", fill="black", font=font)
        return img

    max_val = max(e.value for e in events)
    if max_val == 0:
        max_val = 1.0  # avoid division by zero

    usable_width = PANEL_WIDTH - 2 * MARGIN
    usable_height = PANEL_HEIGHT - 2 * MARGIN
    bar_width = max(1, (usable_width - BAR_GAP * len(events)) // len(events))

    for i, event in enumerate(events):
        bar_height = int((event.value / max_val) * usable_height)
        x0 = MARGIN + i * (bar_width + BAR_GAP)
        y0 = MARGIN + usable_height - bar_height
        x1 = x0 + bar_width
        y1 = MARGIN + usable_height
        draw.rectangle([x0, y0, x1, y1], fill="black")

    return img
