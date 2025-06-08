"""Integration with admin portal for usage logging."""

import asyncio
import json
from typing import Optional
import httpx

from .logger import logger

class AdminLogger:
    """Log usage to admin portal."""
    
    def __init__(self, admin_url: str = "http://localhost:8001"):
        self.admin_url = admin_url.rstrip("/")
        self.enabled = True
    
    async def log_usage(
        self,
        prompt: str,
        response: str,
        model_name: str,
        tokens_used: int = 0,
        embedding_latency_ms: float = 0.0,
        generation_latency_ms: float = 0.0,
        total_latency_ms: float = 0.0,
        user: str = "admin",
        search_mode: str = "hybrid",
        chunks_retrieved: int = 0
    ):
        """Log usage to admin portal asynchronously."""
        if not self.enabled:
            return
        
        try:
            payload = {
                "prompt": prompt,
                "response": response,
                "model_name": model_name,
                "tokens_used": tokens_used,
                "embedding_latency_ms": embedding_latency_ms,
                "generation_latency_ms": generation_latency_ms,
                "total_latency_ms": total_latency_ms,
                "user": user,
                "search_mode": search_mode,
                "chunks_retrieved": chunks_retrieved
            }
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{self.admin_url}/api/usage-log",
                    json=payload
                )
                
                if response.status_code != 200:
                    logger.warning(f"Failed to log usage to admin portal: {response.status_code}")
                    
        except Exception as e:
            logger.warning(f"Failed to log usage to admin portal: {e}")
            # Don't disable logging on error - might be temporary
    
    def log_usage_sync(self, **kwargs):
        """Synchronous wrapper for logging usage."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, schedule the task
                asyncio.create_task(self.log_usage(**kwargs))
            else:
                # If not in async context, run in new loop
                asyncio.run(self.log_usage(**kwargs))
        except Exception as e:
            logger.warning(f"Failed to log usage synchronously: {e}")
    
    def disable(self):
        """Disable admin logging."""
        self.enabled = False
        logger.info("Admin logging disabled")
    
    def enable(self):
        """Enable admin logging."""
        self.enabled = True
        logger.info("Admin logging enabled")

# Global admin logger instance
admin_logger = AdminLogger()