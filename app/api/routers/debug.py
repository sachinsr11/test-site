import asyncio

from fastapi import APIRouter

router = APIRouter()


@router.get("/debug/ping")
async def ping(secs: float = 0.01):
    await asyncio.sleep(secs)
    return {"ping": "ok", "slept": secs}
