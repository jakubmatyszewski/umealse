"""This module is used by pytest for initial configuration that will be applied to tests."""
from beanie import init_beanie
from pytest import fixture
from starlette.config import environ
from httpx import AsyncClient
from src.db import Event, User, Settings
from src.users import current_active_user
from mongomock_motor import AsyncMongoMockClient

from src.main import app
import pytest_asyncio

database_url = (
    f"mongodb://{Settings.DB_USER}:{Settings.DB_PASSWORD}@localhost:{Settings.DB_PORT}"
)
db_client = AsyncMongoMockClient(database_url, connectTimeoutMS=250)


@pytest_asyncio.fixture
async def test_client():
    """
    Yield TestClient instance for tests to use.
    Since scope='session', the fixture is destroyed at the end of the test session.
    """
    await init_beanie(
        database=db_client.test,
        document_models=[User, Event],
    )

    async with AsyncClient(
        app=app, base_url="http://localhost:8080", follow_redirects=True
    ) as ac:
        yield ac


@pytest_asyncio.fixture(name="creds")
async def user_logged_in(test_client: AsyncClient):
    data = {"nickname": "test_acc", "email": "test@example.com", "password": "pass"}
    await test_client.post("/auth/register", json=data)
    creds = {"username": data["email"], "password": data["password"]}

    return creds
