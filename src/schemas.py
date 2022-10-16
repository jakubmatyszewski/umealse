"""Module providing schemas."""
from beanie import PydanticObjectId
from fastapi_users import schemas


class UserRead(schemas.BaseUser[PydanticObjectId]):
    """Provides the basic fields and validation."""


class UserCreate(schemas.BaseUserCreate):
    """Dedicated to user registration. Consists of compulsory email and password fields."""


class UserUpdate(schemas.BaseUserUpdate):
    """Dedicated to user profile update."""
