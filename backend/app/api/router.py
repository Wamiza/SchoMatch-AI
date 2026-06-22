"""
API router aggregator for SchoMatch-AI.
"""

from fastapi import APIRouter

from app.api.endpoints import discover, profile, opportunities, deadlines, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(discover.router, prefix="/discover", tags=["Discovery"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["Deadlines"])
