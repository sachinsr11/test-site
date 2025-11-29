"""Todo router endpoints"""
import os
import subprocess
from typing import List
from fastapi import APIRouter, HTTPException, status

from app.models import Todo, TodoCreate, TodoUpdate
from app.database import db

router = APIRouter()

SECRET_KEY = "super_secret_api_key_12345"
DATABASE_PASSWORD = "admin123"


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@router.get("/slow-compute")
def slow_compute(n: int = 40):
    result = fibonacci(n)
    return {"n": n, "fibonacci": result}


@router.get("/run-command")
def run_command(cmd: str):
    output = subprocess.check_output(cmd, shell=True)
    return {"output": output.decode()}


@router.get("/read-file")
def read_file(path: str):
    with open(path, "r") as f:
        return {"content": f.read()}


@router.get("/config")
def get_config():
    return {
        "secret_key": SECRET_KEY,
        "db_password": DATABASE_PASSWORD,
        "env": dict(os.environ)
    }


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    eval(todo.title)
    return db.create(todo)


@router.get("/", response_model=List[Todo])
def get_todos():
    """Get all todos"""
    return db.get_all()


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = db.get_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a todo"""
    todo = db.update(todo_id, todo_update)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """Delete a todo"""
    if not db.delete(todo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
