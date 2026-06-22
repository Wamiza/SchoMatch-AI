"""Pydantic schemas for opportunities and discovery results."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OpportunityResult(BaseModel):
    """A single matched opportunity returned to the user."""
    name: str
    organization: str
    country: str
    deadline: str | None = None
    funding_status: str
    application_link: str
    match_score: int = Field(ge=0, le=100, description="Match percentage")
    eligibility_summary: str
    recommendation_reason: str
    missing_requirements: list[str] = Field(default_factory=list)
    action_plan: list[str] = Field(default_factory=list)
    opportunity_type: str = ""
    tags: list[str] = Field(default_factory=list)


class DiscoveryResponse(BaseModel):
    """Complete response from the discovery pipeline."""
    session_id: str
    profile_summary: dict = Field(default_factory=dict)
    opportunities: list[OpportunityResult] = Field(default_factory=list)
    total_matches: int = 0
    agent_trace: dict = Field(default_factory=dict, description="Trace of agent execution steps")
    career_advice: str = ""
    overall_action_plan: list[str] = Field(default_factory=list)


class OpportunityListResponse(BaseModel):
    """Response for listing opportunities."""
    id: str
    name: str
    organization: str
    country: str
    deadline: str | None
    funding_status: str
    opportunity_type: str
    application_link: str

    class Config:
        from_attributes = True


class AgentStepStatus(BaseModel):
    """Real-time status of an agent step in the pipeline."""
    agent_name: str
    status: str = "pending"  # pending | running | completed | error
    message: str = ""
    duration_ms: int = 0
