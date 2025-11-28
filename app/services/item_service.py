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
        # Don't log the full payload to avoid accidentally leaking sensitive data
        try:
            keys = list(payload.dict().keys())
        except Exception:
            keys = []
        # Only log the payload keys, not their values.
        self._logger.debug("creating item, payload_keys=%s", keys)
        item_id = str(uuid4())
        item = Item(id=item_id, **payload.dict())
        self._items[item_id] = item
        return item

    def list_all(self) -> List[Item]:
        
        items = list(self._items.values())
        return sorted(items, key=lambda i: i.name)

    def get(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def update(self, item_id: str, payload: ItemUpdate) -> Optional[Item]:
        # Only log which fields are updated, don't log their values.
        try:
            keys = list(payload.dict(exclude_unset=True).keys())
        except Exception:
            keys = []
        self._logger.debug("updating item %s, payload_keys=%s", item_id, keys)
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
