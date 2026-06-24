"""
Agent Runner Service — Executes the ADK multi-agent pipeline.
Provides both synchronous (full result) and streaming (SSE) execution.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, AsyncGenerator

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.api.schemas.opportunity import OpportunityResult, DiscoveryResponse
from app.api.schemas.profile import StudentProfileCreate
from app.config import get_settings

logger = logging.getLogger("schomatch.agent_runner")
settings = get_settings()


# ──────────────────────────────────────────────────────────────
# Tool Functions for Agents
# ──────────────────────────────────────────────────────────────

def analyze_student_profile(
    university: str,
    department: str,
    semester: int,
    gpa: float,
    degree_level: str,
    skills: list[str],
    interests: list[str],
    preferred_countries: list[str],
    opportunity_types: list[str],
    gpa_scale: float = 4.0,
) -> dict:
    """Analyze and structure a student's academic profile for opportunity matching.
    
    Args:
        university: Name of the student's university
        department: Degree program or department
        semester: Current semester number
        gpa: GPA on 4.0 scale
        degree_level: bachelor, master, or phd
        skills: List of student's skills
        interests: List of academic interests
        preferred_countries: Preferred destination countries
        opportunity_types: Types of opportunities sought
    
    Returns:
        Structured profile analysis with strengths and eligibility attributes
    """
    # Normalize GPA to 4.0 scale for uniform evaluation
    normalized_gpa = min(4.0, (gpa / gpa_scale) * 4.0) if gpa_scale > 0 else 0.0

    # Compute academic standing
    if normalized_gpa >= 3.7:
        academic_standing = "excellent"
    elif normalized_gpa >= 3.3:
        academic_standing = "very good"
    elif normalized_gpa >= 3.0:
        academic_standing = "good"
    elif normalized_gpa >= 2.5:
        academic_standing = "average"
    else:
        academic_standing = "below average"

    year_of_study = max(1, (semester + 1) // 2)

    return {
        "status": "success",
        "structured_profile": {
            "university": university,
            "department": department,
            "semester": semester,
            "year_of_study": year_of_study,
            "gpa": gpa,
            "gpa_scale": gpa_scale,
            "normalized_gpa": normalized_gpa,
            "academic_standing": academic_standing,
            "degree_level": degree_level,
            "skills": skills,
            "interests": interests,
            "preferred_countries": preferred_countries,
            "opportunity_types": opportunity_types,
            "strengths": _identify_strengths(gpa, skills, degree_level),
        }
    }


def _identify_strengths(gpa: float, skills: list[str], degree_level: str) -> list[str]:
    """Identify student strengths based on profile."""
    strengths = []
    if gpa >= 3.5:
        strengths.append("Strong academic record")
    if len(skills) >= 5:
        strengths.append("Diverse skill set")
    if any(s.lower() in ["python", "machine learning", "ai", "data science"] for s in skills):
        strengths.append("Technical/STEM skills")
    if any(s.lower() in ["research", "publications", "thesis"] for s in skills):
        strengths.append("Research experience")
    if any(s.lower() in ["leadership", "management", "volunteering"] for s in skills):
        strengths.append("Leadership & service")
    if degree_level in ["master", "phd"]:
        strengths.append("Graduate-level candidate")
    return strengths if strengths else ["Developing academic profile"]


def search_opportunities(
    degree_level: str,
    fields_of_interest: list[str],
    preferred_countries: list[str],
    opportunity_types: list[str],
    min_gpa: float,
) -> dict:
    """Search the opportunity database for matching opportunities.
    
    Args:
        degree_level: Student's degree level (bachelor, master, phd)
        fields_of_interest: Academic fields and interests
        preferred_countries: Preferred destination countries
        opportunity_types: Types of opportunities to search for
        min_gpa: Student's GPA for filtering
    
    Returns:
        List of matching opportunities from the database
    """
    from app.db.seed import SEED_OPPORTUNITIES

    matches = []
    for opp in SEED_OPPORTUNITIES:
        # Check degree level match
        if degree_level not in opp.get("degree_levels", []):
            continue
        
        # Check opportunity type match
        if opportunity_types and opp["opportunity_type"] not in opportunity_types:
            continue
        
        # Check GPA requirement
        opp_min_gpa = opp.get("min_gpa")
        if opp_min_gpa and min_gpa < opp_min_gpa:
            continue

        matches.append({
            "name": opp["name"],
            "organization": opp["organization"],
            "country": opp["country"],
            "deadline": opp.get("deadline", "Rolling"),
            "funding_status": opp["funding_status"],
            "application_link": opp["application_link"],
            "opportunity_type": opp["opportunity_type"],
            "description": opp.get("description", ""),
            "eligibility_summary": opp.get("eligibility_summary", ""),
            "requirements": opp.get("requirements", {}),
            "tags": opp.get("tags", []),
            "min_gpa": opp.get("min_gpa"),
            "fields_of_study": opp.get("fields_of_study", []),
        })

    return {
        "status": "success",
        "total_found": len(matches),
        "opportunities": matches,
    }


def calculate_match_scores(
    student_gpa: float,
    student_degree_level: str,
    student_skills: list[str],
    student_interests: list[str],
    student_countries: list[str],
    opportunities: list[dict],
) -> dict:
    """Calculate match scores between a student profile and opportunities.
    
    Args:
        student_gpa: Student's GPA
        student_degree_level: Student's degree level
        student_skills: Student's skills list
        student_interests: Student's interests
        student_countries: Preferred countries
        opportunities: List of opportunity dictionaries to score
    
    Returns:
        Opportunities with calculated match scores and analysis
    """
    scored = []
    for opp in opportunities:
        score = 0
        missing = []

        # GPA match (25 points)
        opp_min = opp.get("min_gpa")
        if opp_min:
            if student_gpa >= opp_min + 0.5:
                score += 25
            elif student_gpa >= opp_min:
                score += 15
            else:
                score += 5
                missing.append(f"GPA {opp_min}+ recommended (yours: {student_gpa})")
        else:
            score += 20

        # Country match (20 points)
        opp_country = opp.get("country", "")
        if any(c.lower() in opp_country.lower() for c in student_countries):
            score += 20
        elif "global" in opp_country.lower() or "remote" in opp_country.lower() or "multiple" in opp_country.lower():
            score += 15
        else:
            score += 8

        # Field match (25 points)
        opp_fields = opp.get("fields_of_study", [])
        if "all" in opp_fields:
            score += 22
        elif any(
            any(interest.lower() in f.lower() or f.lower() in interest.lower() 
                for f in opp_fields)
            for interest in student_interests
        ):
            score += 25
        else:
            score += 10
            missing.append("Consider aligning your field with opportunity requirements")

        # Skills match (15 points)
        opp_reqs = opp.get("requirements", {})
        req_skills = opp_reqs.get("skills", "")
        if req_skills:
            if any(s.lower() in req_skills.lower() for s in student_skills):
                score += 15
            else:
                score += 5
                missing.append(f"Develop skills: {req_skills}")
        else:
            score += 12

        # Funding bonus (5 points)
        if "fully funded" in opp.get("funding_status", "").lower():
            score += 5
        else:
            score += 3

        # Prestige bonus (10 points)
        if "prestigious" in opp.get("tags", []):
            score += 8
        else:
            score += 5

        scored.append({
            **opp,
            "match_score": min(score, 100),
            "missing_requirements": missing,
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return {"status": "success", "scored_opportunities": scored}


def generate_career_advice(
    student_profile: dict,
    top_opportunities: list[dict],
) -> dict:
    """Generate personalized career advice and action plans based on matched opportunities.
    
    Args:
        student_profile: Structured student profile dictionary
        top_opportunities: Top matched opportunities with scores
    
    Returns:
        Career advice, improvement suggestions, and application roadmap
    """
    advice_items = []
    action_plan = []

    gpa = student_profile.get("gpa", 0)
    skills = student_profile.get("skills", [])
    degree = student_profile.get("degree_level", "bachelor")

    # GPA-based advice
    if gpa < 3.0:
        advice_items.append("Focus on improving your GPA — many top scholarships require 3.0+")
        action_plan.append("Prioritize academic performance this semester")
    elif gpa < 3.5:
        advice_items.append("Your GPA is competitive for many programs. Consider targeting 3.5+ for elite scholarships.")

    # Skills-based advice
    if len(skills) < 3:
        advice_items.append("Build a broader skill set — take online courses, workshops, or certifications")
        action_plan.append("Complete at least 2 relevant online certifications in the next 3 months")

    # Degree-based advice
    if degree == "bachelor":
        advice_items.append("As an undergraduate, focus on research experience and internships to strengthen graduate applications")
        action_plan.append("Seek out a research assistant position with a professor in your department")

    # Opportunity-based advice
    if top_opportunities:
        earliest_deadline = sorted(
            [o for o in top_opportunities if o.get("deadline") and o["deadline"] != "Rolling"],
            key=lambda x: x["deadline"]
        )
        if earliest_deadline:
            action_plan.append(f"Start with '{earliest_deadline[0]['name']}' — deadline: {earliest_deadline[0]['deadline']}")
        
        action_plan.append("Prepare a strong personal statement tailored to each application")
        action_plan.append("Gather recommendation letters from professors familiar with your work")
        action_plan.append("Verify English proficiency test requirements (TOEFL/IELTS) for international programs")

    return {
        "status": "success",
        "career_advice": " | ".join(advice_items) if advice_items else "Your profile is strong — focus on applying strategically.",
        "action_plan": action_plan,
    }


def register_deadlines(opportunities: list[dict]) -> dict:
    """Register and organize deadlines from matched opportunities.
    
    Args:
        opportunities: List of opportunities with deadline information
    
    Returns:
        Organized deadline schedule with reminders
    """
    deadlines = []
    for opp in opportunities:
        dl = opp.get("deadline", "Rolling")
        if dl and dl != "Rolling":
            deadlines.append({
                "opportunity": opp["name"],
                "deadline": dl,
                "organization": opp.get("organization", ""),
                "reminder_30_days": True,
                "reminder_7_days": True,
            })

    deadlines.sort(key=lambda x: x["deadline"])
    return {
        "status": "success",
        "total_deadlines": len(deadlines),
        "deadlines": deadlines,
    }


# ──────────────────────────────────────────────────────────────
# ADK Agent Definitions
# ──────────────────────────────────────────────────────────────

def _build_agents():
    """Build the multi-agent pipeline using Google ADK."""
    model = settings.PRIMARY_MODEL

    profile_agent = LlmAgent(
        name="profile_analysis_agent",
        model=model,
        description="Analyzes and structures student academic profiles for opportunity matching.",
        instruction="""You are a Profile Analysis specialist. Your job is to analyze a student's raw input 
and create a structured academic profile. Use the analyze_student_profile tool with the student's data.
Extract all relevant information and identify the student's strengths and eligibility attributes.
Always call the tool with the exact data provided — do not make up or assume information.""",
        tools=[analyze_student_profile],
        output_key="structured_profile",
    )

    discovery_agent = LlmAgent(
        name="opportunity_discovery_agent",
        model=model,
        description="Searches for scholarships, internships, and academic opportunities matching a student profile.",
        instruction="""You are an Opportunity Discovery specialist. Using the structured profile from the previous step,
search for matching opportunities. Use the search_opportunities tool with the student's degree level, 
interests, preferred countries, desired opportunity types, and GPA.
Report all matching opportunities found.""",
        tools=[search_opportunities],
        output_key="raw_opportunities",
    )

    eligibility_agent = LlmAgent(
        name="eligibility_matching_agent",
        model=model,
        description="Compares opportunity requirements with student profiles and generates match scores.",
        instruction="""You are an Eligibility Matching specialist. Using the student profile and discovered opportunities,
calculate match scores for each opportunity. Use the calculate_match_scores tool.
Pass the student's GPA, degree level, skills, interests, preferred countries, and the list of opportunities.
Rank opportunities by match score from highest to lowest.""",
        tools=[calculate_match_scores],
        output_key="ranked_results",
    )

    career_agent = LlmAgent(
        name="career_advisor_agent",
        model=model,
        description="Provides personalized career advice and application strategies.",
        instruction="""You are a Career Advisor specialist. Based on the student profile and top-matched opportunities,
provide personalized career advice and an action plan. Use the generate_career_advice tool.
Explain why each top opportunity was recommended and suggest specific steps to improve the student's profile.""",
        tools=[generate_career_advice],
        output_key="career_advice",
    )

    deadline_agent = LlmAgent(
        name="deadline_tracker_agent",
        model=model,
        description="Organizes deadlines and creates a reminder schedule.",
        instruction="""You are a Deadline Tracking specialist. From the ranked opportunities, 
extract and organize all deadlines. Use the register_deadlines tool.
Create a timeline of upcoming deadlines so the student can plan their applications.""",
        tools=[register_deadlines],
        output_key="deadline_schedule",
    )

    orchestrator = SequentialAgent(
        name="schomatch_orchestrator",
        sub_agents=[profile_agent, discovery_agent, eligibility_agent, career_agent, deadline_agent],
        description="Orchestrates the full ScholarAgent pipeline from profile analysis to deadline tracking.",
    )

    return orchestrator


# ──────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────

async def run_discovery_pipeline(profile: StudentProfileCreate) -> DiscoveryResponse:
    """Execute the full multi-agent discovery pipeline."""
    start_time = time.time()
    session_id = str(uuid.uuid4())
    agent_trace = {}

    try:
        orchestrator = _build_agents()
        session_service = InMemorySessionService()
        
        runner = Runner(
            agent=orchestrator,
            app_name="schomatch_ai",
            session_service=session_service,
        )

        session = await session_service.create_session(
            app_name="schomatch_ai",
            user_id="student_user",
        )

        # Build the user message with profile data
        user_message = f"""Please analyze this student profile and find matching opportunities:

University: {profile.university}
Department: {profile.department}
Semester: {profile.semester}
GPA: {profile.gpa}
Degree Level: {profile.degree_level}
Skills: {', '.join(profile.skills)}
Interests: {', '.join(profile.interests)}
Preferred Countries: {', '.join(profile.preferred_countries)}
Opportunity Types: {', '.join(profile.opportunity_types)}

Please process this through the full pipeline: analyze the profile, search for opportunities, 
calculate match scores, provide career advice, and register deadlines."""

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        )

        # Collect agent responses
        final_text_parts = []
        agent_trace["steps"] = []
        
        async for event in runner.run_async(
            user_id="student_user",
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_text_parts.append(part.text)
                    if hasattr(part, 'function_call') and part.function_call:
                        agent_trace["steps"].append({
                            "tool": part.function_call.name,
                            "status": "called",
                        })
                    if hasattr(part, 'function_response') and part.function_response:
                        agent_trace["steps"].append({
                            "tool": part.function_response.name,
                            "status": "completed",
                        })

        # Parse results from the pipeline
        opportunities = await _extract_opportunities_from_session(profile, session_service, session.id)
        career_advice_text = _extract_career_advice(final_text_parts)

        elapsed = time.time() - start_time
        agent_trace["total_duration_ms"] = int(elapsed * 1000)
        agent_trace["agents_executed"] = [
            "profile_analysis_agent",
            "opportunity_discovery_agent", 
            "eligibility_matching_agent",
            "career_advisor_agent",
            "deadline_tracker_agent",
        ]

        return DiscoveryResponse(
            session_id=session_id,
            profile_summary={
                "university": profile.university,
                "department": profile.department,
                "gpa": profile.gpa,
                "degree_level": profile.degree_level,
            },
            opportunities=opportunities,
            total_matches=len(opportunities),
            agent_trace=agent_trace,
            career_advice=career_advice_text,
            overall_action_plan=_build_overall_action_plan(profile, opportunities),
        )

    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        # Fallback: run tools directly without ADK agent orchestration
        return await _fallback_pipeline(profile, session_id, start_time, str(e))


async def _fallback_pipeline(
    profile: StudentProfileCreate, session_id: str, start_time: float, error_msg: str
) -> DiscoveryResponse:
    """Fallback pipeline that runs tools directly if ADK agents fail."""
    logger.info("Running fallback pipeline (direct tool execution)...")

    # Step 1: Profile analysis
    profile_result = analyze_student_profile(
        university=profile.university,
        department=profile.department,
        semester=profile.semester,
        gpa=profile.gpa,
        degree_level=profile.degree_level,
        skills=profile.skills,
        interests=profile.interests,
        preferred_countries=profile.preferred_countries,
        opportunity_types=profile.opportunity_types,
        gpa_scale=profile.gpa_scale,
    )

    # Step 2: Search
    search_result = search_opportunities(
        degree_level=profile.degree_level,
        fields_of_interest=profile.interests,
        preferred_countries=profile.preferred_countries,
        opportunity_types=profile.opportunity_types,
        min_gpa=profile.gpa,
    )

    # Step 3: Scoring
    score_result = calculate_match_scores(
        student_gpa=profile.gpa,
        student_degree_level=profile.degree_level,
        student_skills=profile.skills,
        student_interests=profile.interests,
        student_countries=profile.preferred_countries,
        opportunities=search_result["opportunities"],
    )

    # Step 4: Career advice
    career_result = generate_career_advice(
        student_profile=profile_result["structured_profile"],
        top_opportunities=score_result["scored_opportunities"][:5],
    )

    # Step 5: Deadlines
    deadline_result = register_deadlines(score_result["scored_opportunities"])

    # Build response
    opportunities = [
        OpportunityResult(
            name=opp["name"],
            organization=opp["organization"],
            country=opp["country"],
            deadline=opp.get("deadline", "Rolling"),
            funding_status=opp["funding_status"],
            application_link=opp["application_link"],
            match_score=opp["match_score"],
            eligibility_summary=opp.get("eligibility_summary", ""),
            recommendation_reason=_generate_recommendation_reason(opp, profile),
            missing_requirements=opp.get("missing_requirements", []),
            action_plan=career_result.get("action_plan", []),
            opportunity_type=opp.get("opportunity_type", ""),
            tags=opp.get("tags", []),
        )
        for opp in score_result["scored_opportunities"]
    ]

    elapsed = time.time() - start_time

    return DiscoveryResponse(
        session_id=session_id,
        profile_summary={
            "university": profile.university,
            "department": profile.department,
            "gpa": profile.gpa,
            "degree_level": profile.degree_level,
            "academic_standing": profile_result["structured_profile"]["academic_standing"],
        },
        opportunities=opportunities,
        total_matches=len(opportunities),
        agent_trace={
            "mode": "fallback",
            "error": error_msg,
            "total_duration_ms": int((time.time() - start_time) * 1000),
            "agents_executed": [
                "profile_analysis_agent",
                "opportunity_discovery_agent",
                "eligibility_matching_agent",
                "career_advisor_agent",
                "deadline_tracker_agent",
            ],
        },
        career_advice=career_result.get("career_advice", ""),
        overall_action_plan=career_result.get("action_plan", []),
    )


async def _extract_opportunities_from_session(
    profile: StudentProfileCreate, session_service, session_id: str
) -> list[OpportunityResult]:
    """Extract structured opportunities from agent session state.
    
    Attempts to read output_key values stored by ADK agents first.
    Falls back to direct tool execution only if session state is empty.
    """
    try:
        # Try reading from ADK session state (agents store via output_key)
        session = await session_service.get_session(
            app_name="schomatch_ai",
            user_id="student_user",
            session_id=session_id,
        )

        state = getattr(session, "state", {}) or {}
        ranked_results = state.get("ranked_results")
        career_advice_state = state.get("career_advice")

        if ranked_results:
            # Parse ranked results — may be a JSON string or dict
            if isinstance(ranked_results, str):
                try:
                    ranked_results = json.loads(ranked_results)
                except json.JSONDecodeError:
                    ranked_results = None

        if ranked_results and isinstance(ranked_results, dict):
            scored = ranked_results.get("scored_opportunities", [])
            if scored:
                # Parse career advice for action plan
                action_plan = []
                if career_advice_state:
                    if isinstance(career_advice_state, str):
                        try:
                            career_advice_state = json.loads(career_advice_state)
                        except json.JSONDecodeError:
                            career_advice_state = {}
                    if isinstance(career_advice_state, dict):
                        action_plan = career_advice_state.get("action_plan", [])

                logger.info(f"Read {len(scored)} opportunities from ADK session state")
                return [
                    OpportunityResult(
                        name=opp["name"],
                        organization=opp["organization"],
                        country=opp["country"],
                        deadline=opp.get("deadline", "Rolling"),
                        funding_status=opp["funding_status"],
                        application_link=opp["application_link"],
                        match_score=opp["match_score"],
                        eligibility_summary=opp.get("eligibility_summary", ""),
                        recommendation_reason=_generate_recommendation_reason(opp, profile),
                        missing_requirements=opp.get("missing_requirements", []),
                        action_plan=action_plan,
                        opportunity_type=opp.get("opportunity_type", ""),
                        tags=opp.get("tags", []),
                    )
                    for opp in scored
                ]
    except Exception as e:
        logger.warning(f"Could not read ADK session state, falling back to direct tools: {e}")

    # Fallback: re-run tools directly
    logger.info("Falling back to direct tool execution for opportunity extraction")
    search_result = search_opportunities(
        degree_level=profile.degree_level,
        fields_of_interest=profile.interests,
        preferred_countries=profile.preferred_countries,
        opportunity_types=profile.opportunity_types,
        min_gpa=profile.gpa,
    )

    score_result = calculate_match_scores(
        student_gpa=profile.gpa,
        student_degree_level=profile.degree_level,
        student_skills=profile.skills,
        student_interests=profile.interests,
        student_countries=profile.preferred_countries,
        opportunities=search_result["opportunities"],
    )

    career_result = generate_career_advice(
        student_profile={"gpa": profile.gpa, "skills": profile.skills, "degree_level": profile.degree_level},
        top_opportunities=score_result["scored_opportunities"][:5],
    )

    return [
        OpportunityResult(
            name=opp["name"],
            organization=opp["organization"],
            country=opp["country"],
            deadline=opp.get("deadline", "Rolling"),
            funding_status=opp["funding_status"],
            application_link=opp["application_link"],
            match_score=opp["match_score"],
            eligibility_summary=opp.get("eligibility_summary", ""),
            recommendation_reason=_generate_recommendation_reason(opp, profile),
            missing_requirements=opp.get("missing_requirements", []),
            action_plan=career_result.get("action_plan", []),
            opportunity_type=opp.get("opportunity_type", ""),
            tags=opp.get("tags", []),
        )
        for opp in score_result["scored_opportunities"]
    ]


def _generate_recommendation_reason(opp: dict, profile: StudentProfileCreate) -> str:
    """Generate a human-readable recommendation reason."""
    reasons = []
    if "fully funded" in opp.get("funding_status", "").lower():
        reasons.append("Fully funded opportunity")
    if any(c.lower() in opp.get("country", "").lower() for c in profile.preferred_countries):
        reasons.append(f"Located in your preferred country: {opp.get('country', '')}")
    if opp.get("min_gpa") and profile.gpa >= opp["min_gpa"]:
        reasons.append(f"Your GPA ({profile.gpa}) meets the minimum requirement ({opp['min_gpa']})")
    if "prestigious" in opp.get("tags", []):
        reasons.append("Highly prestigious program")
    if profile.degree_level in opp.get("degree_levels", []):
        reasons.append(f"Open to {profile.degree_level} students")
    return ". ".join(reasons) if reasons else "Matches your profile criteria"


def _extract_career_advice(text_parts: list[str]) -> str:
    """Extract career advice from agent text output."""
    combined = " ".join(text_parts)
    return combined if combined else "Focus on applying early to maximize your chances."


def _build_overall_action_plan(
    profile: StudentProfileCreate, opportunities: list[OpportunityResult]
) -> list[str]:
    """Build an overall action plan from profile and matched opportunities."""
    plan = [
        f"Review your {len(opportunities)} matched opportunities below",
        "Prioritize opportunities with the highest match scores",
        "Prepare core application documents: CV, transcripts, recommendation letters",
    ]
    
    if profile.gpa < 3.5:
        plan.append("Work on improving your GPA to qualify for more competitive programs")
    
    plan.extend([
        "Tailor your personal statement for each application",
        "Start applications well before deadlines — aim for 4-6 weeks lead time",
        "Follow up with recommenders 2 weeks before each deadline",
    ])
    
    return plan
