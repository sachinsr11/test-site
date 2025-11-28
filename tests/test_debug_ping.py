import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_debug_ping(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/debug/ping?secs=0.01")
    assert resp.status_code == 200
    assert resp.json()["ping"] == "ok"
