"""Tests for the opportunities endpoint."""

import pytest


@pytest.mark.asyncio
async def test_list_opportunities(client):
    """GET /api/opportunities should return 200 with a list."""
    response = await client.get("/api/opportunities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_opportunities_with_pagination(client):
    """Pagination params should be accepted."""
    response = await client.get("/api/opportunities?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
