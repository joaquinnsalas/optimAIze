#!/usr/bin/env python3
"""API server entrypoint for OptimAIze."""

import os
import uvicorn
from src.retrieval.api import app
from src.utils.logger import logger

# Set environment variables
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

if __name__ == "__main__":
    logger.info("Starting OptimAIze API server...")
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )