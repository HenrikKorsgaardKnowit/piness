"""Tests for the sysinfo panel."""

from PIL import Image

from piness.display.panels.sysinfo import render_sysinfo, PANEL_WIDTH, PANEL_HEIGHT


class TestSysinfoPanel:
    def test_returns_correct_size(self):
        img = render_sysinfo(hostname="testhost", ip_address="10.0.0.1")
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)

    def test_returns_rgb_image(self):
        img = render_sysinfo(hostname="testhost", ip_address="10.0.0.1")
        assert img.mode == "RGB"

    def test_renders_without_args(self):
        """Should use real hostname/IP without crashing."""
        img = render_sysinfo()
        assert isinstance(img, Image.Image)

    def test_custom_values_do_not_crash(self):
        img = render_sysinfo(hostname="a" * 100, ip_address="255.255.255.255")
        assert img.size == (PANEL_WIDTH, PANEL_HEIGHT)
