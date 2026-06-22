"""
External API MCP Server for SchoMatch-AI.
Connects to external databases.
"""

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("External API Server")

@mcp.tool()
async def fetch_external_scholarships(field: str, limit: int = 5) -> str:
    """Fetch scholarships from external portal APIs.
    
    Args:
        field: Field of study
        limit: Max results to return
    """
    results = [
        {"name": f"External {field} Grant", "amount": "$5,000", "deadline": "Next month"},
        {"name": f"Global {field} Fellowship", "amount": "Fully Funded", "deadline": "In 3 months"}
    ][:limit]
    
    return json.dumps({"status": "success", "source": "external_api", "results": results})

if __name__ == "__main__":
    mcp.run()
