"""
Deadlines endpoints.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def placeholder_deadlines():
    return {"message": "Deadline endpoints to be implemented"}
