from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Get health status")
async def health() -> dict:
    """Return a simple health check response."""
    return {"status": "ok"}
