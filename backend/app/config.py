"""Load settings from environment variables.

CognoDB values are read here so the next phase can connect without
changing the rest of the app. They are optional in this phase.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")


def _csv_env(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    """Runtime configuration. Secrets come from the environment only."""

    app_name: str
    app_env: str
    cors_origins: list[str]
    cognodb_uri: str
    cognodb_user: str
    cognodb_password: str

    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "Student Skill Career Graph API")
        self.app_env = os.getenv("APP_ENV", "development")
        self.cors_origins = _csv_env(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000",
        )
        # Empty strings until the database phase is configured.
        self.cognodb_uri = os.getenv("COGNODB_URI", "")
        self.cognodb_user = os.getenv("COGNODB_USER", "")
        self.cognodb_password = os.getenv("COGNODB_PASSWORD", "")


settings = Settings()
