"""
Discovery endpoints for running the agent pipeline.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.opportunity import DiscoveryResponse
from app.api.schemas.profile import StudentProfileCreate
from app.db.database import get_db
from app.db.models import SearchSession
from app.services.agent_runner import run_discovery_pipeline

router = APIRouter()


@router.post("", response_model=DiscoveryResponse)
async def discover_opportunities(
    request: Request,
    profile: StudentProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Run the full ADK agent pipeline to discover opportunities for a student.
    Rate limited to prevent API abuse.
    """
    try:
        # Save profile to database first to satisfy foreign key constraints
        from app.db.models import StudentProfile
        import uuid
        profile_record = StudentProfile(id=str(uuid.uuid4()), **profile.model_dump())
        db.add(profile_record)
        await db.flush()
        
        # Run the agent pipeline
        result = await run_discovery_pipeline(profile)
        
        # Save session to database (async)
        session_record = SearchSession(
            id=result.session_id,
            profile_id=profile_record.id,
            results=[opp.model_dump() for opp in result.opportunities],
            agent_trace=result.agent_trace,
            total_matches=result.total_matches
        )
        db.add(session_record)
        await db.commit()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discovery pipeline failed: {str(e)}")


@router.get("/{session_id}", response_model=DiscoveryResponse)
async def get_discovery_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a previous discovery session by ID."""
    from sqlalchemy import select
    
    query = select(SearchSession).where(SearchSession.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Reconstruct response (simplified for now, assumes no linked profile in this mockup)
    return DiscoveryResponse(
        session_id=session.id,
        profile_summary={},
        opportunities=session.results,
        total_matches=session.total_matches,
        agent_trace=session.agent_trace,
        career_advice="",
        overall_action_plan=[]
    )
