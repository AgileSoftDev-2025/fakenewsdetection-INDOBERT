#!/bin/bash
# Railway start script - Auto-migrate database with delay, then start server

# Wait for PostgreSQL to be ready
echo "⏳ Waiting 10 seconds for PostgreSQL to be ready..."
sleep 10

# Run database migration
echo "Running database migration..."
python migrate_to_db.py

# Start FastAPI server
echo "Starting FastAPI server on port ${PORT:-8000}..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
