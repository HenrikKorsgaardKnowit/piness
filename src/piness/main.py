"""Entrypoint for the piness service: API + display refresh loop."""

import threading
import time

import uvicorn

from piness.api.server import create_app
from piness.config import load_settings
from piness.display.panels.graph import render_graph
from piness.display.panels.messages import render_messages
from piness.display.panels.sysinfo import render_sysinfo
from piness.display.renderer import Renderer
from piness.store import EventBuffer, MessageBuffer


def _make_driver(mock: bool):
    if mock:
        from piness.display.driver import MockDriver
        return MockDriver()
    else:
        from piness.display.driver import InkyDriver
        return InkyDriver()


class RefreshScheduler:
    """Debounced display refresh triggered by data changes.

    When notify() is called, waits `debounce` seconds for more changes
    before actually refreshing. Only one refresh runs at a time.
    """

    def __init__(self, renderer: Renderer, debounce: float = 5.0):
        self._renderer = renderer
        self._debounce = debounce
        self._pending = threading.Event()
        self._lock = threading.Lock()

    def notify(self):
        """Signal that data has changed. Refresh will happen after debounce period."""
        self._pending.set()

    def run(self):
        """Main loop — blocks forever. Run in a daemon thread."""
        while True:
            # Wait until something signals a change
            self._pending.wait()
            # Debounce: wait a bit for more changes to arrive
            self._pending.clear()
            time.sleep(self._debounce)
            # Drain any additional signals that arrived during debounce
            self._pending.clear()

            with self._lock:
                try:
                    self._renderer.render()
                    print("Display refreshed")
                except Exception as e:
                    print(f"Display refresh error: {e}")


def main() -> None:
    settings = load_settings()

    event_buf = EventBuffer(maxlen=100)
    message_buf = MessageBuffer(maxlen=50)

    driver = _make_driver(settings.mock_display)
    renderer = Renderer(
        driver=driver,
        sysinfo_panel=render_sysinfo,
        graph_panel=lambda: render_graph(event_buf.items()),
        messages_panel=lambda: render_messages(message_buf.latest(1)),
    )

    # Initial render (forced)
    renderer.render(force=True)
    print(f"piness started (mock={settings.mock_display})")

    scheduler = RefreshScheduler(renderer, debounce=5.0)

    # Start refresh scheduler in background
    refresh_thread = threading.Thread(target=scheduler.run, daemon=True)
    refresh_thread.start()

    # Start API server (blocks), pass scheduler so routes can trigger refresh
    app = create_app(
        event_buffer=event_buf,
        message_buffer=message_buf,
        refresh_scheduler=scheduler,
    )
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)


if __name__ == "__main__":
    main()
