"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os


@dataclass
class Settings:
    """Application settings with defaults suitable for local development."""

    pi_host: str = ""
    pi_user: str = ""
    pi_password: str = ""
    pi_deploy_path: str = "/home/pi/piness"
    display_width: int = 400
    display_height: int = 300
    refresh_interval: int = 60
    api_port: int = 8080
    mock_display: bool = True


def load_settings(env_path: str | Path | None = None) -> Settings:
    """Load settings from .env file and environment variables."""
    load_dotenv(dotenv_path=env_path)

    return Settings(
        pi_host=os.getenv("PI_HOST", ""),
        pi_user=os.getenv("PI_USER", ""),
        pi_password=os.getenv("PI_PASSWORD", ""),
        pi_deploy_path=os.getenv("PI_DEPLOY_PATH", "/home/pi/piness"),
        display_width=int(os.getenv("DISPLAY_WIDTH", "400")),
        display_height=int(os.getenv("DISPLAY_HEIGHT", "300")),
        refresh_interval=int(os.getenv("REFRESH_INTERVAL", "60")),
        api_port=int(os.getenv("API_PORT", "8080")),
        mock_display=os.getenv("MOCK_DISPLAY", "true").lower() in ("true", "1", "yes"),
    )
