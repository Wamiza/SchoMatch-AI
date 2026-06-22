"""
SchoMatch-AI — FastAPI Application Entry Point
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.router import api_router
from app.config import get_settings
from app.db.database import init_db
from app.middleware.rate_limiter import limiter

logger = logging.getLogger("schomatch")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    settings = get_settings()
    logger.info("🚀 SchoMatch-AI starting up...")
    logger.info(f"   Primary model: {settings.PRIMARY_MODEL}")
    logger.info(f"   Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'SQLite'}")

    # Initialize database
    await init_db()
    logger.info("   Database initialized ✓")

    yield

    logger.info("👋 SchoMatch-AI shutting down...")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title="SchoMatch-AI",
        description=(
            "AI-powered platform that helps students discover personalized "
            "scholarships, internships, research opportunities, fellowships, "
            "exchange programs, and summer schools worldwide."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Rate Limiting ---
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # --- Routers ---
    app.include_router(api_router, prefix="/api")

    return app


# Create the app instance
app = create_app()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
