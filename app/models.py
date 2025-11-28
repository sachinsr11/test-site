"""Data models for Todo API"""
from pydantic import BaseModel, Field
from typing import Optional


class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False


class TodoUpdate(BaseModel):
    """Schema for updating a todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    """Complete todo model with ID"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True
