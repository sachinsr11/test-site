import os
import time

from fastapi import APIRouter, Header, HTTPException

router = APIRouter()


@router.get("/debug/echo_auth")
async def echo_auth(authorization: str | None = Header(None)):
    """Echo back the Authorization header value; insecure (leaks tokens)."""
    return {"authorization": authorization}


@router.get("/debug/env")
async def dump_env():
    """Return environment variables — intentional security leak for testing."""
    # caution: this endpoint exposes all environment variables
    return dict(os.environ)


@router.get("/debug/sleep")
async def blocking_sleep(secs: float = 0.5):
    """Blocking sleep inside async handler to simulate an event-loop blocking bug."""
    time.sleep(secs)
    return {"slept": secs}


@router.get("/debug/eval")
async def eval_expr(expr: str):
    """Eval user-provided expressions (RCE) — intentionally insecure."""
    try:
        result = eval(expr)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"result": str(result)}
