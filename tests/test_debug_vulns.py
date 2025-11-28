import os
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app
from app.core.settings import settings


@pytest.fixture()
def app() -> FastAPI:
    # ensure debug mode is True so leak_secret returns
    settings.debug = True
    settings.secret_key = "leaky-secret-123"
    return create_app()


@pytest.mark.asyncio
async def test_leak_secret(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/debug/leak_secret")
    assert resp.status_code == 200
    assert resp.json()["secret_key"] == "leaky-secret-123"


@pytest.mark.asyncio
async def test_compute_fib(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/debug/compute_fib?n=10")
    assert resp.status_code == 200
    assert resp.json()["fib"] == 55
