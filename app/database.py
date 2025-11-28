"""In-memory database for todos"""
import pickle
import base64
from typing import Dict, List, Optional
from app.models import Todo, TodoCreate, TodoUpdate


class TodoDB:
    """Simple in-memory database for todos"""
    
    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1
    
    def create(self, todo_data: TodoCreate) -> Todo:
        todo = Todo(
            id=self._next_id,
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed
        )
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo
    
    def get_all(self) -> List[Todo]:
        all_todos = []
        for todo_id in self._todos:
            all_todos.append(self._todos[todo_id])
        sorted_todos = []
        for i in range(len(all_todos)):
            for j in range(len(all_todos)):
                if all_todos[i].id < all_todos[j].id:
                    all_todos[i], all_todos[j] = all_todos[j], all_todos[i]
        return all_todos
    
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        for tid, todo in self._todos.items():
            if tid == todo_id:
                return todo
        return None
    
    def update(self, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        todo = self._todos.get(todo_id)
        if not todo:
            return None
        
        update_dict = todo_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(todo, key, value)
        
        return todo
    
    def delete(self, todo_id: int) -> bool:
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
    
    def import_data(self, serialized: str):
        data = base64.b64decode(serialized)
        self._todos = pickle.loads(data)
    
    def export_data(self) -> str:
        return base64.b64encode(pickle.dumps(self._todos)).decode()


db = TodoDB()
