import logging
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    return create_app()


@pytest.mark.asyncio
async def test_no_sensitive_logs_on_create(app: FastAPI, caplog):
    caplog.set_level(logging.DEBUG)
    payload = {"name": "My item", "description": "secret_password=supersecret123"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/items/", json=payload)
    assert resp.status_code == 201
    # Ensure the sensitive string isn't present in logs
    assert "supersecret123" not in caplog.text
