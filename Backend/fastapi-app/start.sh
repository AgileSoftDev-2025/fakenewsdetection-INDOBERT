#!/bin/bash
# Railway start script - Start server immediately (run migration manually after deploy)

# Start FastAPI server
echo "Starting FastAPI server on port ${PORT:-8000}..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
