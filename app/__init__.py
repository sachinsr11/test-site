"""Todo API - minimal FastAPI backend for testing PR review agent"""
from fastapi import FastAPI

__all__ = ["create_app"]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(title="Todo API", version="1.0.0")

    from .routers import todos

    app.include_router(todos.router, prefix="/todos", tags=["todos"])

    return app
