# Test Site - FastAPI example

A simple FastAPI app used for tests and demos.

## Running locally

Install dependencies and run with Uvicorn:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Visit:
- http://localhost:8000/health
- http://localhost:8000/items/

## Running tests

```bash
pip install -r requirements.txt
pytest -q
```

Or use the provided script:

```bash
./run_dev.sh  # runs the dev server
```

## Project layout

- `app/` - FastAPI application package
- `tests/` - pytest tests
