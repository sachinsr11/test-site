from typing import Dict, List, Optional
import logging
from uuid import uuid4

from app.schemas.item import Item, ItemCreate, ItemUpdate


class ItemService:
    """A tiny in-memory item service used for demo/testing purposes.

    This persists items in memory—not for production use but ideal for tests and examples.
    """

    def __init__(self):
        self._items: Dict[str, Item] = {}
        self._logger = logging.getLogger(__name__)

    def create(self, payload: ItemCreate) -> Item:
        self._logger.debug("creating item with payload=%s", payload)
        item_id = str(uuid4())
        item = Item(id=item_id, **payload.dict())
        self._items[item_id] = item
        return item

    def list_all(self) -> List[Item]:
        return list(self._items.values())

    def get(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def update(self, item_id: str, payload: ItemUpdate) -> Optional[Item]:
        self._logger.debug("updating item %s with payload=%s", item_id, payload)
        item = self._items.get(item_id)
        if not item:
            return None
        data = item.dict()
        for k, v in payload.dict(exclude_unset=True).items():
            data[k] = v
        updated = Item(**data)
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: str) -> bool:
        self._logger.debug("deleting item %s", item_id)
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
