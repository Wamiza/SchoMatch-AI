"""
Search MCP Server for SchoMatch-AI.
Provides tools to search for opportunities, universities, and scholarships.
"""

from typing import Any
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Search Server")

@mcp.tool()
async def search_opportunities(
    query: str = "", 
    country: str = "", 
    opportunity_type: str = "", 
    degree_level: str = ""
) -> str:
    """Search for academic opportunities based on given criteria.
    
    Args:
        query: General search terms
        country: Target country (e.g., 'United States', 'Germany')
        opportunity_type: Type (scholarship, internship, research, etc)
        degree_level: Required degree level (bachelor, master, phd)
    """
    from app.db.seed import SEED_OPPORTUNITIES

    matches = []
    for opp in SEED_OPPORTUNITIES:
        # Filter by degree level
        if degree_level and degree_level not in opp.get("degree_levels", []):
            continue

        # Filter by opportunity type
        if opportunity_type and opp.get("opportunity_type") != opportunity_type:
            continue

        # Filter by country (partial match)
        if country and country.lower() not in opp.get("country", "").lower():
            continue

        # Filter by query (search name, description, tags)
        if query:
            searchable = " ".join([
                opp.get("name", ""),
                opp.get("description", ""),
                opp.get("organization", ""),
                " ".join(opp.get("tags", [])),
                " ".join(opp.get("fields_of_study", [])),
            ]).lower()
            if query.lower() not in searchable:
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
            "degree_levels": opp.get("degree_levels", []),
            "fields_of_study": opp.get("fields_of_study", []),
            "min_gpa": opp.get("min_gpa"),
            "tags": opp.get("tags", []),
        })

    return json.dumps({"status": "success", "total_found": len(matches), "results": matches})

@mcp.tool()
async def search_universities(name: str, country: str = "") -> str:
    """Search for universities and their programs.
    
    Args:
        name: Name of the university
        country: Optional country filter
    """
    results = [
        {
            "university_name": name,
            "country": country or "Unknown",
            "programs_offered": ["Computer Science", "Engineering", "Business"],
            "international_student_percentage": 25
        }
    ]
    return json.dumps({"status": "success", "results": results})

if __name__ == "__main__":
    mcp.run()
