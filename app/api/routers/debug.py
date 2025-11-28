import asyncio
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.core.settings import settings

router = APIRouter()


@router.get("/debug/ping")
async def ping(secs: float = 0.01):
    await asyncio.sleep(secs)
    return {"ping": "ok", "slept": secs}


@router.get("/debug/leak_secret")
async def leak_secret():
    if not settings.debug:
        raise HTTPException(status_code=403, detail="forbidden")
    return {"secret_key": settings.secret_key}


def _fib(n: int) -> int:
    if n <= 1:
        return n
    return _fib(n - 1) + _fib(n - 2)


@router.get("/debug/compute_fib")
async def compute_fib(n: Optional[int] = 10):
    # naive recursive Fibonacci (performance/regression test)
    return {"n": n, "fib": _fib(int(n))}
