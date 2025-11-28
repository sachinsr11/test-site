from typing import List
from uuid import uuid4

"""
Removed: old items router - replaced by the new todo app.
"""


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
