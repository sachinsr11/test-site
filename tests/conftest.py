"""Pytest configuration"""
import os
import sys
import pytest

# Ensure repository root is importable as a module root (so `import app` works)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    from app.database import db
    db._todos.clear()
    db._next_id = 1
    yield
