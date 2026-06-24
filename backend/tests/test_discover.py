"""Tests for the discovery pipeline endpoint."""

import pytest


VALID_PROFILE = {
    "university": "Test University",
    "department": "Computer Science",
    "semester": 6,
    "gpa": 3.8,
    "degree_level": "bachelor",
    "skills": ["Python", "Machine Learning"],
    "interests": ["Artificial Intelligence"],
    "preferred_countries": ["United States"],
    "opportunity_types": ["scholarship", "internship"],
}


@pytest.mark.asyncio
async def test_discover_requires_profile(client):
    """POST /api/discover without a body should return 422."""
    response = await client.post("/api/discover")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_discover_rejects_invalid_gpa(client):
    """GPA outside valid range should be rejected."""
    bad_profile = {**VALID_PROFILE, "gpa": 5.0, "gpa_scale": 4.0}
    response = await client.post("/api/discover", json=bad_profile)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_discover_rejects_invalid_degree(client):
    """Invalid degree_level should be rejected."""
    bad_profile = {**VALID_PROFILE, "degree_level": "associate"}
    response = await client.post("/api/discover", json=bad_profile)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_session_not_found(client):
    """GET /api/discover/{bad_id} should return 404."""
    response = await client.get("/api/discover/nonexistent-session-id")
    assert response.status_code == 404
