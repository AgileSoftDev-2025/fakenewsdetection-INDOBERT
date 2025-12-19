#!/bin/bash
# Railway start script - Auto-migrate database then start server

# Run database migration on startup (creates tables if not exist)
echo "Running database migration..."
python migrate_to_db.py

# Start FastAPI server
echo "Starting FastAPI server on port ${PORT:-8000}..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
