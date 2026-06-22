import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        res = await client.get("http://localhost:8000/api/opportunities")
        print("Opportunities:", res.status_code, res.text)
        
        payload = {
            "university": "Stanford",
            "department": "CS",
            "semester": 6,
            "gpa": 3.8,
            "degree_level": "bachelor",
            "skills": ["Python"],
            "interests": ["AI"],
            "preferred_countries": ["US"],
            "opportunity_types": ["scholarship"]
        }
        res2 = await client.post("http://localhost:8000/api/discover", json=payload, timeout=30.0)
        print("Discover:", res2.status_code)
        print(res2.text[:500])

asyncio.run(test())
