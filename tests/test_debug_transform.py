import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_transform_eval(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        expr = "lambda s: s[::-1]"
        resp = await ac.get(f"/debug/transform?expr={expr}&value=abc")
    assert resp.status_code == 200
    assert resp.json()["result"] == "cba"
