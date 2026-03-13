"""Messages panel showing the most recent text messages."""

from PIL import Image, ImageDraw, ImageFont

from piness.store import Message

PANEL_WIDTH = 400
PANEL_HEIGHT = 100
MARGIN = 10
LINE_HEIGHT = 20
MAX_VISIBLE = 4


def render_messages(messages: list[Message]) -> Image.Image:
    """Return a Pillow Image with the most recent messages.

    Shows up to MAX_VISIBLE messages, most recent first.
    An empty list produces a blank panel with a placeholder label.
    """
    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    if not messages:
        draw.text(
            (MARGIN, PANEL_HEIGHT // 2 - 8), "no messages", fill="black", font=font
        )
        return img

    # Show newest first, limited to what fits
    visible = messages[:MAX_VISIBLE]
    for i, msg in enumerate(visible):
        prefix = f"[{msg.source}] " if msg.source else ""
        text = f"{prefix}{msg.text}"
        # Truncate long lines
        if len(text) > 50:
            text = text[:47] + "..."
        y = MARGIN + i * LINE_HEIGHT
        draw.text((MARGIN, y), text, fill="black", font=font)

    return img
