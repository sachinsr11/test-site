from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., example="My Item")
    description: Optional[str] = Field(None, example="A description of the item")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    special_code: Optional[str] = None


class Item(ItemBase):
    id: str

    class Config:
        orm_mode = True
