"""Test events."""
import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from src.db import Event


async def create_test_event() -> Event:
    event = Event(
        owner="test_acc",
        datetime=datetime.now() + timedelta(9),
        description="test",
        event_name="test",
        private=False,
        recipy_url="",
    )

    output = await event.insert()
    return output


@pytest.mark.asyncio
async def test_add_event(test_client: AsyncClient, creds: dict):
    data = {
        "owner": "test_acc",
        "datetime": str(datetime.now() + timedelta(9)),
        "description": "some description",
        "event_name": "test",
        "private": False,
        "recipy_url": "",
        "attendants": [],
    }
    output = await test_client.post("/events/add", json=data)
    assert output.status_code == 401

    # Log in, grab auth token
    x = await test_client.post("/auth/jwt/login", data=creds)
    token = x.json()["access_token"]

    output = await test_client.post(
        "/events/add", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    # Correct request
    assert output.status_code == 201

    # Assert validation fails when user is not an owner
    bad_owner_data = data
    bad_owner_data["owner"] = "nonexistant_user"
    output = await test_client.post(
        "/events/add", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert output.status_code == 400

    # Assert validation fails when event in the past
    bad_date_data = data
    bad_date_data["datetime"] = str(datetime.now() + timedelta(-2))
    output = await test_client.post(
        "/events/add", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert output.status_code == 400


@pytest.mark.asyncio
async def test_get_event(test_client: AsyncClient, creds: dict):
    test_event = await create_test_event()
    test_event_id = test_event.id

    output = await test_client.get(f"/events/{test_event_id}")
    # Assert login is required
    assert output.status_code == 401

    login_data = await test_client.post("/auth/jwt/login", data=creds)
    token = login_data.json()["access_token"]

    output = await test_client.get(
        f"/events/{test_event_id}", headers={"Authorization": f"Bearer {token}"}
    )
    # Correct request
    assert output.status_code == 200

    output = await test_client.get(
        f"/events/Ba4d_1id", headers={"Authorization": f"Bearer {token}"}
    )
    # Assert request fails if bad id is passed
    assert output.status_code == 400


@pytest.mark.asyncio
async def test_get_event_list(test_client: AsyncClient):
    pass
    # """Get list of events."""

    # limit = 10
    # skip = page * limit
    # events = await Event.find({}, skip=skip, limit=limit, sort="datetime").to_list()
    # return events


@pytest.mark.asyncio
async def test_update_event(test_client: AsyncClient):
    pass
    # """Update an event."""
    # event = await get_event_by_id(id)
    # validation = new_event_validator(data, user)
    # if validation.status != Status.OK:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    #     return validation

    # if isinstance(event, Event):
    #     data_dict = data.dict()
    #     for key in data_dict.keys():
    #         new_value = getattr(data, key)
    #         setattr(event, key, new_value)

    #     await event.save()
    #     return StatusMessage(status=Status.OK, message=f"Event updated")

    # response.status_code = status.HTTP_400_BAD_REQUEST
    # return event


@pytest.mark.asyncio
async def test_delete_event(test_client: AsyncClient):
    pass
    # """Delete an event."""

    # event = await get_event_by_id(id)

    # if isinstance(event, Event):
    #     if user.username != event.owner:
    #         response.status_code = status.HTTP_401_UNAUTHORIZED
    #         return StatusMessage(
    #             status=Status.ERROR, message="Current user must be an Event owner."
    #         )
    #     return StatusMessage(status=Status.OK, message=f"Event {id} deleted.")
    # return event
