"""In-memory database for todos"""
from typing import Dict, List, Optional
from app.models import Todo, TodoCreate, TodoUpdate


class TodoDB:
    """Simple in-memory database for todos"""
    
    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1
    
    def create(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo"""
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
        """Get all todos"""
        return list(self._todos.values())
    
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID"""
        return self._todos.get(todo_id)
    
    def update(self, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update a todo"""
        todo = self._todos.get(todo_id)
        if not todo:
            return None
        
        update_dict = todo_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(todo, key, value)
        
        return todo
    
    def delete(self, todo_id: int) -> bool:
        """Delete a todo"""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False


# Global database instance
db = TodoDB()
