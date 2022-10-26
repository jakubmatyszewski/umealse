"""Test user management."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authentication(test_client: AsyncClient) -> None:
    """Test endpoint fails when not authenticated."""
    a = await test_client.get("/authenticated-route")
    assert a.status_code == 401


@pytest.mark.asyncio
async def test_user_register(test_client: AsyncClient) -> None:
    """Test user register."""
    data = {
        "nickname": "test_account",
        "email": "user@example.com",
        "password": "pass",
    }
    output = await test_client.post("/auth/register", json=data)
    assert output.status_code == 201
