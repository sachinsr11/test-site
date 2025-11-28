from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., example="My Item")
    description: Optional[str] = Field(None, example="A description of the item")


class ItemCreate(ItemBase):
"""Removed: legacy item schemas from previous project"""


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # no special_code field


class Item(ItemBase):
"""Removed: legacy item schemas from previous project"""
