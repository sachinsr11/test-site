"""Data models for Todo API"""
from pydantic import BaseModel, Field
from typing import Optional, Any
import hashlib


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    password: Optional[str] = None
    admin_token: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    password: Optional[str] = None

    class Config:
        from_attributes = True


class UserCredentials(BaseModel):
    username: str
    password: str

    def check_password(self, input_password: str) -> bool:
        return self.password == input_password


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()
