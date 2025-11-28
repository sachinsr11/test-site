"""Test suite for Todo API"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture()
def app() -> FastAPI:
    """Create a fresh app instance for each test"""
    return create_app()


@pytest.mark.asyncio
async def test_create_todo(app: FastAPI):
    """Test creating a new todo"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/todos/",
            json={"title": "Test todo", "description": "Test description"}
        )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_get_all_todos(app: FastAPI):
    """Test getting all todos"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a todo first
        await client.post("/todos/", json={"title": "Todo 1"})
        await client.post("/todos/", json={"title": "Todo 2"})
        
        # Get all todos
        response = await client.get("/todos/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


@pytest.mark.asyncio
async def test_get_todo_by_id(app: FastAPI):
    """Test getting a specific todo"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a todo
        create_response = await client.post(
            "/todos/",
            json={"title": "Test todo"}
        )
        todo_id = create_response.json()["id"]
        
        # Get the todo
        response = await client.get(f"/todos/{todo_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test todo"


@pytest.mark.asyncio
async def test_get_nonexistent_todo(app: FastAPI):
    """Test getting a todo that doesn't exist"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/todos/9999")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo(app: FastAPI):
    """Test updating a todo"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a todo
        create_response = await client.post(
            "/todos/",
            json={"title": "Original title", "completed": False}
        )
        todo_id = create_response.json()["id"]
        
        # Update the todo
        response = await client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated title", "completed": True}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_todo(app: FastAPI):
    """Test deleting a todo"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a todo
        create_response = await client.post(
            "/todos/",
            json={"title": "To be deleted"}
        )
        todo_id = create_response.json()["id"]
        
        # Delete the todo
        delete_response = await client.delete(f"/todos/{todo_id}")
        assert delete_response.status_code == 204
        
        # Verify it's gone
        get_response = await client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_todo(app: FastAPI):
    """Test deleting a todo that doesn't exist"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/todos/9999")
    
    assert response.status_code == 404
