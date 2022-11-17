"""Test events."""
import json
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
async def test_get_event_list(test_client: AsyncClient, creds: dict):
    # create a test event
    await create_test_event()

    output = await test_client.get("/events/list/0")
    # Assert login is required
    assert output.status_code == 401

    login_data = await test_client.post("/auth/jwt/login", data=creds)
    token = login_data.json()["access_token"]

    output = await test_client.get(
        "/events/list/0", headers={"Authorization": f"Bearer {token}"}
    )
    # Correct request
    assert output.status_code == 200
    assert len(output.json()) == 1

    output = await test_client.get(
        "/events/list/1", headers={"Authorization": f"Bearer {token}"}
    )
    # 10 entries per page
    # when there is 1 event, ensure that nothing is returned on page 1
    assert len(output.json()) == 0

    # add 11 events (12 overall)
    for _ in range(11):
        await create_test_event()

    output = await test_client.get(
        "/events/list/1", headers={"Authorization": f"Bearer {token}"}
    )
    # when there are overall 12 events, ensure that on page 1 there are 2 events returned
    assert len(output.json()) == 2

    output = await test_client.get(
        f"/events/list/Ba4d_1id", headers={"Authorization": f"Bearer {token}"}
    )
    # Assert request fails if param provided is not an int
    assert output.status_code == 422


@pytest.mark.asyncio
async def test_update_event(test_client: AsyncClient, creds: dict):
    test_event = await create_test_event()
    test_event_id = test_event.id
    
    new_data = json.loads(test_event.json())
    # Remove `revision_id` from db addition call
    del new_data["revision_id"]
    new_data["event_name"] = "new event name"

    output = await test_client.put(f"/events/{test_event_id}", json=new_data)
    # Assert login is required
    assert output.status_code == 401

    login_data = await test_client.post("/auth/jwt/login", data=creds)
    token = login_data.json()["access_token"]

    output = await test_client.put(
        f"/events/{test_event_id}", headers={"Authorization": f"Bearer {token}"}, json=new_data
    )
    # Correct request
    assert output.status_code == 200
    assert output.json()["data"]["event_name"] == "new event name"

    new_data = {
        "owner": "test_acc",
        "datetime": str(datetime.now() + timedelta(10)),
        "description": "new description",
        "event_name": "new event name",
        "private": True,
        "recipy_url": "http://google.com",
        "attendants": []
    }

    output = await test_client.put(
        f"/events/{test_event_id}", headers={"Authorization": f"Bearer {token}"}, json=new_data
    )
    assert output.status_code == 200

    output = await test_client.put(
        f"/events/Ba4d_1id", headers={"Authorization": f"Bearer {token}"}, json=new_data
    )
    # Assert request fails if bad id is passed
    assert output.status_code == 400


@pytest.mark.asyncio
async def test_delete_event(test_client: AsyncClient, creds: dict):
    test_event = await create_test_event()
    test_event_id = test_event.id

    output = await test_client.delete(f"/events/{test_event_id}")
    # Assert login is required
    assert output.status_code == 401

    login_data = await test_client.post("/auth/jwt/login", data=creds)
    token = login_data.json()["access_token"]

    output = await test_client.delete(
        f"/events/{test_event_id}", headers={"Authorization": f"Bearer {token}"}
    )
    # Correct request
    assert output.status_code == 200

    output = await test_client.delete(
        f"/events/Ba4d_1id", headers={"Authorization": f"Bearer {token}"}
    )
    # Assert request fails if bad id is passed
    assert output.status_code == 400
