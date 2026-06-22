"""
Opportunities endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas.opportunity import OpportunityListResponse
from app.db.database import get_db
from app.db.models import Opportunity

router = APIRouter()

@router.get("", response_model=list[OpportunityListResponse])
async def list_opportunities(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List available opportunities in the database."""
    query = select(Opportunity).offset(skip).limit(limit)
    result = await db.execute(query)
    opportunities = result.scalars().all()
    
    return [
        OpportunityListResponse(
            id=o.id,
            name=o.name,
            organization=o.organization,
            country=o.country,
            deadline=o.deadline,
            funding_status=o.funding_status,
            opportunity_type=o.opportunity_type,
            application_link=o.application_link
        )
        for o in opportunities
    ]
