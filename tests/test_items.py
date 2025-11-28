import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_items_crud(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Initially empty
        resp = await ac.get("/items/")
        assert resp.status_code == 200
        assert resp.json() == []

        # create
        payload = {"name": "My item", "description": "some desc"}
        resp = await ac.post("/items/", json=payload)
        assert resp.status_code == 201
        item = resp.json()
        assert item["name"] == payload["name"]
        assert item["description"] == payload["description"]
        item_id = item["id"]

        # list
        resp = await ac.get("/items/")
        assert resp.status_code == 200
        items = resp.json()
        assert any(i["id"] == item_id for i in items)

        # get
        resp = await ac.get(f"/items/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == item_id

        # update
        resp = await ac.put(f"/items/{item_id}", json={"name": "New Name"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

        # delete
        resp = await ac.delete(f"/items/{item_id}")
        assert resp.status_code == 204

        # ensure gone
        resp = await ac.get(f"/items/{item_id}")
        assert resp.status_code == 404
