"""
Module for db connection.
"""
import os
import motor.motor_asyncio
from beanie import Document, PydanticObjectId
from datetime import datetime
from dotenv import load_dotenv
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from mongomock_motor import AsyncMongoMockClient
from typing import Optional, List

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

database_url = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
client = motor.motor_asyncio.AsyncIOMotorClient(
    database_url, uuidRepresentation="standard"
)

if "TESTING" in os.environ.keys():
    client = AsyncMongoMockClient()

database = client[DB_NAME]


class User(BeanieBaseUser[PydanticObjectId]):
    """DB User model, inheriting base fields from FastAPI Users module."""

    username: str


class Event(Document):
    """DB Event model."""

    owner: str
    datetime: Optional[datetime]
    description: str
    event_name: str
    private: bool
    recipy_url: Optional[str]
    attendants: List = []

    class Settings:
        name = "Event"


async def get_user_db():
    """
    The database adapter of FastAPI Users, link between db configuration and the users logic.
    Gets called by FastAPI Depends.
    """
    yield BeanieUserDatabase(User)
