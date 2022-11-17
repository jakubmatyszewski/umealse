"""User managements endpoints."""
from bson import errors as bson_errors
from beanie import PydanticObjectId
from datetime import datetime, timedelta
from fastapi import APIRouter, Response, status

from src.users import current_active_user
from fastapi import Depends
from src.db import Event, User
from src.schemas import EventCreate, EventUpdate
from src.utils import Status, StatusMessage
from typing import Union, List

event_router = APIRouter()


async def get_event_by_id(id: str) -> Union[Event, StatusMessage]:
    try:
        _id = PydanticObjectId(id)
    except bson_errors.InvalidId:
        return StatusMessage(
            status=Status.ERROR,
            message=f"{id} is a wrong Event id.",
        )
    event = await Event.find_one({"_id": _id})
    if event:
        return event

    return StatusMessage(
        status=Status.ERROR, message=f"Could not find event with id: {id}"
    )


def new_event_validator(data: Union[EventCreate, EventUpdate], user: User) -> StatusMessage:
    """Set of rules to ensure correct data is passed while creating an event."""
    if user.nickname != data.owner:
        return StatusMessage(
            status=Status.ERROR, message="Current user must be an Event owner."
        )
    dt = data.datetime.replace(tzinfo=None)
    if dt - datetime.now() < timedelta(0):
        return StatusMessage(
            status=Status.ERROR, message="Event can not happen in the past."
        )
    return StatusMessage(status=Status.OK, message="Validation successfull.")


@event_router.post("/events/add")
async def add_event(
    data: EventCreate,
    response: Response,
    user: User = Depends(current_active_user),
) -> StatusMessage:
    """Create an event."""

    validation = new_event_validator(data, user)
    if validation.status != Status.OK:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return validation

    event = Event(
        owner=data.owner,
        datetime=data.datetime,
        description=data.description,
        event_name=data.event_name,
        private=data.private,
        recipy_url=data.recipy_url,
    )

    output = await event.insert()
    response.status_code = status.HTTP_201_CREATED

    return StatusMessage(status=Status.OK, message=f"Event created. id: {output.id}")


@event_router.get("/events/{id}", status_code=200)
async def get_event(
    id: str, response: Response, user: User = Depends(current_active_user)
) -> Union[Event, StatusMessage]:
    """Read an event."""

    event = await get_event_by_id(id)
    if isinstance(event, Event):
        if event.private:
            # check if user is an owner or attends in the event
            if user not in event.attendants or event.owner != user:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return StatusMessage(
                    status=Status.ERROR,
                    message=f"User not authorized to access this event.",
                )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

    # Output is either Event or error
    return event


@event_router.get("/events/list/{page}", status_code=200)
async def get_event_list(
    page: int,
    user: User = Depends(current_active_user),
) -> List[Event]:
    """Get list of events."""

    limit = 10
    skip = page * limit
    events = await Event.find({}, skip=skip, limit=limit, sort="datetime").to_list()
    return events


@event_router.put("/events/{id}", status_code=200)
async def update_event(
    id: str,
    data: EventUpdate,
    response: Response,
    user: User = Depends(current_active_user),
) -> StatusMessage:
    """Update an event."""
    get_event_output = await get_event_by_id(id)
    validation = new_event_validator(data, user)
    if validation.status != Status.OK:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return validation

    if isinstance(get_event_output, Event):
        data_dict = data.dict()
        for key in data_dict.keys():
            new_value = getattr(data, key)
            setattr(get_event_output, key, new_value)

        await get_event_output.save()
        return StatusMessage(status=Status.OK, message=f"Event updated", data=get_event_output)

    response.status_code = status.HTTP_400_BAD_REQUEST
    return get_event_output


@event_router.delete("/events/{id}", status_code=200)
async def delete_event(
    id: str, response: Response, user: User = Depends(current_active_user)
) -> StatusMessage:
    """Delete an event."""

    get_event_output = await get_event_by_id(id)

    if isinstance(get_event_output, Event):
        if user.nickname != get_event_output.owner:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return StatusMessage(
                status=Status.ERROR, message="Current user must be an Event owner."
            )
        return StatusMessage(status=Status.OK, message=f"Event {id} deleted.")

    response.status_code = status.HTTP_400_BAD_REQUEST
    return get_event_output
