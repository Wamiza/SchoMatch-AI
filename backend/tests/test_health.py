"""Tests for the health endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Health endpoint should return 200 with status ok."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
