#!/usr/bin/env bash
set -euo pipefail

# Run development server: ensure you have installed requirements
python -m uvicorn app.main:app --reload --port 8000
