"""
SchoMatch-AI Configuration
Loads settings from environment variables / .env file
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Google AI ---
    GOOGLE_API_KEY: str = ""
    PRIMARY_MODEL: str = "gemini-2.0-flash"
    REASONING_MODEL: str = "gemini-2.5-flash"

    # --- Database ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./schomatch.db"

    # --- Server ---
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # --- Rate Limiting ---
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # --- Security ---
    SECRET_KEY: str = "dev-secret-change-in-production"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    # Try loading .env from backend directory or project root
    env_paths = [
        Path(__file__).parent.parent / ".env",
        Path(__file__).parent.parent.parent / ".env",
    ]
    for p in env_paths:
        if p.exists():
            os.environ.setdefault("ENV_FILE", str(p))
            break
    return Settings()
