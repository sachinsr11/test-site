from typing import List
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.item import ItemCreate, Item, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter()

service = ItemService()


@router.post("/", response_model=Item, status_code=201)
async def create_item(payload: ItemCreate) -> Item:
    return service.create(payload)


@router.get("/", response_model=List[Item])
async def list_items() -> List[Item]:
    return service.list_all()


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: str) -> Item:
    item = service.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: str, payload: ItemUpdate) -> Item:
    item = service.update(item_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str):
    deleted = service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
