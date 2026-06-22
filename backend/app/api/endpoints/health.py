"""
Health check endpoints.
"""

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "SchoMatch-AI Backend",
        "primary_model": settings.PRIMARY_MODEL
    }
