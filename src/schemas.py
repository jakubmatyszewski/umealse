"""Module providing schemas."""
from beanie import PydanticObjectId
from fastapi_users import schemas
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserRead(schemas.BaseUser[PydanticObjectId]):
    """Provides the basic fields and validation."""


class UserCreate(schemas.BaseUserCreate):
    """Dedicated to user registration. Consists of compulsory email and password fields."""


class UserUpdate(schemas.BaseUserUpdate):
    """Dedicated to user profile update."""


class EventRead:
    pass


class EventCreate(BaseModel):
    """Schema dedicated to creating an event."""

    owner: str
    datetime: datetime
    description: str
    event_name: str
    private: bool = False
    recipy_url: Optional[str] = ""


class EventUpdate:
    pass


class EventDelete:
    pass
