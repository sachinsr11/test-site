import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_read_file_traversal(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # attempt to read a file outside the base dir by using relative path
        path = "..%2Ftests%2Fsecret_file.txt"
        resp = await ac.get(f"/debug/read_file?path={path}")
    assert resp.status_code == 200
    assert "TOP_SECRET_CONTENT" in resp.json()["content"]
