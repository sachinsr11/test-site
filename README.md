# Todo API

A minimal FastAPI backend for testing PR review agents.

## Features

- Create, read, update, and delete todos
- In-memory storage (no database required)
- Simple RESTful API

## Endpoints

- `POST /todos/` - Create a new todo
- `GET /todos/` - Get all todos
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the interactive API documentation.

## Running tests

```bash
pytest
```

## Project layout

- `app/` - FastAPI application package
  - `models.py` - Pydantic models
  - `database.py` - In-memory database
  - `routers/todos.py` - Todo endpoints
- `tests/` - pytest tests
