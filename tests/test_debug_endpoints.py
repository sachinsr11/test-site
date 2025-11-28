import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_debug_endpoints_removed_and_ping_exists(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/debug/echo_auth")
        assert resp.status_code == 404
        resp = await ac.get("/debug/env")
        assert resp.status_code == 404
        resp = await ac.get("/debug/eval?expr=1+2")
        assert resp.status_code == 404
        resp = await ac.get("/debug/exec_cmd?cmd=echo+hello")
        assert resp.status_code == 404
        # ping should exist and respond
        resp = await ac.get("/debug/ping?secs=0.01")
        assert resp.status_code == 200
        assert resp.json()["ping"] == "ok"
