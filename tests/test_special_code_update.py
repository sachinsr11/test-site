import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_special_code_not_supported(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"name": "My item", "description": "desc"}
        resp = await ac.post("/items/", json=payload)
        assert resp.status_code == 201
        item = resp.json()
        item_id = item["id"]
        # special_code is not accepted; ensure it doesn't get executed and results in 422 or ignored
        resp = await ac.put(f"/items/{item_id}", json={"special_code": "1+2"})
        # We can't be certain how the API rejects it; assert 200 and confirm name unchanged or 422
        if resp.status_code == 200:
            assert resp.json()["name"] == "My item"
        else:
            assert resp.status_code == 422
