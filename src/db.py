"""
Module for db connection.
"""
import os
import motor.motor_asyncio
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from dotenv import load_dotenv

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
database = client[DB_NAME]
if "TESTING" in os.environ.keys():
    database = client["TEST"]


class User(BeanieBaseUser[PydanticObjectId]):
    """User model for db inheriting base fields from FastAPI Users."""


async def get_user_db():
    """
    The database adapter of FastAPI Users, link between db configuration and the users logic.
    Gets called by FastAPI Depends.
    """
    yield BeanieUserDatabase(User)
