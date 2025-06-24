#!/bin/bash

# Simple startup without complex dependency management
echo "Starting OptimAIze Teams Bot..."

# Set the port
export PORT=${PORT:-8000}

# Start the application directly
python -m uvicorn app:app --host 0.0.0.0 --port $PORT --log-level info