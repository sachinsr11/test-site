import asyncio
from typing import Optional

from fastapi import APIRouter, Header

router = APIRouter()


@router.get("/debug/ping")
async def ping(secs: float = 0.01):
    await asyncio.sleep(secs)
    return {"ping": "ok", "slept": secs}


@router.get("/debug/headers")
async def headers(authorization: str | None = Header(None)):
    return {"authorization": authorization}
