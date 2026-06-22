"""
Profile endpoints.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def placeholder_profile():
    return {"message": "Profile endpoints to be implemented"}
