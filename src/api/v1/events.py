"""User managements endpoints."""
from datetime import datetime, timedelta
from fastapi import APIRouter

# from fastapi.responses import JSONResponse
from src.users import current_active_user
from fastapi import Depends
from src.db import Event, User
from src.schemas import EventCreate
from src.utils import Status, StatusMessage

event_router = APIRouter()


def new_event_validator(data: EventCreate, user: User) -> StatusMessage:
    """Set of rules to ensure correct data is passed while creating an event."""
    if user.username != data.owner:
        return StatusMessage(
            status=Status.ERROR, message="Current user must be an Event owner."
        )
    dt = data.datetime.replace(tzinfo=None)
    if dt - datetime.now() < timedelta(0):
        return StatusMessage(
            status=Status.ERROR, message="Unable to create Event in the past."
        )
    return StatusMessage(status=Status.OK, message="Validation successfull.")


@event_router.post("/event/add")
async def add_event(data: EventCreate, user: User = Depends(current_active_user)):
    """Endpoint to test if authentication works."""

    validation = new_event_validator(data, user)
    if validation.status == Status.OK:
        event = Event(
            owner=data.owner,
            datetime=data.datetime,
            description=data.description,
            event_name=data.event_name,
            private=data.private,
            recipy_url=data.recipy_url,
        )

        response = await event.insert()

        if response.id:
            return StatusMessage(
                status=Status.OK, message=f"Event created. id: {response.id}"
            )

    return validation
