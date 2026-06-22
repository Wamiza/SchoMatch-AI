"""
Knowledge MCP Server for SchoMatch-AI.
Provides tools for eligibility rules, country requirements, and funding info.
"""

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knowledge Server")

@mcp.tool()
async def get_eligibility_rules(opportunity_type: str, degree_level: str) -> str:
    """Get general eligibility rules for a type of opportunity.
    
    Args:
        opportunity_type: Type of opportunity (scholarship, internship, etc)
        degree_level: Current degree level
    """
    rules = {
        "general_requirements": ["Valid passport", "Academic transcripts"],
        "language_requirements": "Usually IELTS 6.5+ or TOEFL 90+",
        "gpa_expectation": "Typically 3.0+ for standard, 3.5+ for competitive",
    }
    return json.dumps({"status": "success", "rules": rules})

@mcp.tool()
async def get_country_requirements(country: str) -> str:
    """Get specific visa and student requirements for a country.
    
    Args:
        country: The target country
    """
    reqs = {
        "country": country,
        "student_visa_required": True,
        "proof_of_funds_required": True,
        "work_allowed_on_student_visa": "Usually up to 20 hours/week during term",
    }
    return json.dumps({"status": "success", "requirements": reqs})

if __name__ == "__main__":
    mcp.run()
