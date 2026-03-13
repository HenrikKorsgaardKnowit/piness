"""Messages panel showing the most recent message."""

from PIL import Image, ImageDraw, ImageFont

from piness.store import Message

PANEL_WIDTH = 380
PANEL_HEIGHT = 88
MARGIN = 8


def render_messages(messages: list[Message]) -> Image.Image:
    """Return a full-width Pillow Image with the most recent message (up to 140 chars)."""
    img = Image.new("RGB", (PANEL_WIDTH, PANEL_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        font = ImageFont.load_default()

    if not messages:
        draw.text((MARGIN, PANEL_HEIGHT // 2 - 10), "no messages", fill="black", font=font)
        return img

    latest = messages[0]
    prefix = f"[{latest.source}] " if latest.source else ""
    text = f"{prefix}{latest.text}"
    if len(text) > 140:
        text = text[:137] + "..."

    # Word wrap using pixel width
    max_width = PANEL_WIDTH - 2 * MARGIN
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        test_bbox = draw.textbbox((0, 0), test, font=font)
        if test_bbox[2] - test_bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        y = MARGIN + i * 18
        if y + 18 > PANEL_HEIGHT - 4:
            break
        draw.text((MARGIN, y), line, fill="black", font=font)

    return img
