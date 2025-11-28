# app package
from fastapi import FastAPI

__all__ = ["create_app"]


def create_app() -> FastAPI:
    """Return a FastAPI application instance used by run scripts and tests."""
    app = FastAPI(title="Test Site API", version="0.1.0")

    # Import routers here to create lazy import boundaries
    from .api.routers import health, items, debug

    app.include_router(health)
    app.include_router(items, prefix="/items", tags=["items"])

    app.include_router(debug)

    return app
