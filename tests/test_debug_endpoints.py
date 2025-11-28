import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_debug_echo_auth(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/debug/echo_auth", headers={"Authorization": "Bearer secret-token-123"})
    assert resp.status_code == 200
    # Intentionally expecting the API to echo back the token
    assert resp.json()["authorization"] == "Bearer secret-token-123"


@pytest.mark.asyncio
async def test_debug_env(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/debug/env")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)


@pytest.mark.asyncio
async def test_debug_sleep(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # use a small sleep to keep tests fast
        resp = await ac.get("/debug/sleep?secs=0.01")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_debug_eval(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/debug/eval", params={"expr": "1+2"})
    assert resp.status_code == 200
    assert resp.json()["result"] == "3"
