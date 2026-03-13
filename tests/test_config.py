"""Tests for configuration loading."""

import os
from pathlib import Path

import pytest

from piness.config import Settings, load_settings


class TestSettingsDefaults:
    def test_default_values(self):
        s = Settings()
        assert s.display_width == 400
        assert s.display_height == 300
        assert s.refresh_interval == 60
        assert s.api_port == 8080
        assert s.mock_display is True
        assert s.pi_deploy_path == "/home/pi/piness"

    def test_custom_values(self):
        s = Settings(display_width=800, mock_display=False, api_port=9090)
        assert s.display_width == 800
        assert s.mock_display is False
        assert s.api_port == 9090


class TestLoadSettings:
    def test_loads_from_env_file(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PI_HOST=192.168.1.100\n"
            "PI_USER=pi\n"
            "PI_PASSWORD=secret\n"
            "MOCK_DISPLAY=false\n"
            "API_PORT=3000\n"
        )
        settings = load_settings(env_path=str(env_file))
        assert settings.pi_host == "192.168.1.100"
        assert settings.pi_user == "pi"
        assert settings.pi_password == "secret"
        assert settings.mock_display is False
        assert settings.api_port == 3000

    def test_defaults_when_no_env_file(self, tmp_path, monkeypatch):
        # Clear any existing env vars that would interfere
        for key in ("PI_HOST", "PI_USER", "PI_PASSWORD", "MOCK_DISPLAY", "API_PORT"):
            monkeypatch.delenv(key, raising=False)
        settings = load_settings(env_path=str(tmp_path / "nonexistent"))
        assert settings.pi_host == ""
        assert settings.mock_display is True

    def test_env_vars_override(self, monkeypatch):
        monkeypatch.setenv("DISPLAY_WIDTH", "800")
        monkeypatch.setenv("REFRESH_INTERVAL", "30")
        settings = load_settings()
        assert settings.display_width == 800
        assert settings.refresh_interval == 30
