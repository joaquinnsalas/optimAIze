"""
FastAPI wrapper for Azure App Service deployment

This module provides a FastAPI interface for the OptimAIze Teams Bot
to ensure compatibility with Azure App Service deployment.
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response
import structlog
from bot import init_bot_app
import asyncio

# Configure logging
logger = structlog.get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="OptimAIze Teams Bot",
    description="Microsoft Teams bot integration for OptimAIze RAG system",
    version="1.0.0"
)

# Global reference to the aiohttp bot app
bot_app = None

@app.on_event("startup")
async def startup_event():
    """Initialize the bot application on startup"""
    global bot_app
    try:
        logger.info("Starting OptimAIze Teams Bot...")
        bot_app = await init_bot_app()
        logger.info("OptimAIze Teams Bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint - redirect to health check"""
    return {"service": "OptimAIze Teams Bot", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if bot_app:
        # Create a mock aiohttp request to call the bot's health handler
        from aiohttp.web import Request as AiohttpRequest
        from aiohttp.test_utils import make_mocked_request
        
        mock_request = make_mocked_request('GET', '/health')
        
        # Get the health handler from bot app
        health_handler = None
        for route in bot_app.router.routes():
            if route.resource and hasattr(route.resource, '_path') and route.resource._path == '/health':
                health_handler = route._handler
                break
        
        if health_handler:
            try:
                response = await health_handler(mock_request)
                return response.body if hasattr(response, 'body') else {"status": "healthy"}
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return {"status": "error", "error": str(e)}
    
    return {"status": "bot_not_initialized"}

@app.post("/api/messages")
async def messages_endpoint(request: Request):
    """Handle Teams bot messages"""
    if not bot_app:
        return Response(status_code=503, content="Bot not initialized")
    
    try:
        # Get the messages handler from the bot app
        messages_handler = None
        for route in bot_app.router.routes():
            if (route.resource and 
                hasattr(route.resource, '_path') and 
                route.resource._path == '/api/messages'):
                messages_handler = route._handler
                break
        
        if not messages_handler:
            return Response(status_code=500, content="Messages handler not found")
        
        # Convert FastAPI request to aiohttp request format
        body = await request.body()
        headers = dict(request.headers)
        
        # Create mock aiohttp request
        from aiohttp.test_utils import make_mocked_request
        from aiohttp.web import Request as AiohttpRequest
        import json
        
        mock_request = make_mocked_request(
            'POST', 
            '/api/messages',
            headers=headers,
            payload=body
        )
        
        # Process the request
        response = await messages_handler(mock_request)
        
        return Response(
            status_code=response.status,
            content=response.body if hasattr(response, 'body') else None,
            headers=dict(response.headers) if hasattr(response, 'headers') else {}
        )
        
    except Exception as e:
        logger.error(f"Error processing Teams message: {e}")
        return Response(status_code=500, content=f"Error: {str(e)}")

@app.get("/status")
async def status_endpoint():
    """Detailed status endpoint"""
    if not bot_app:
        return {"status": "bot_not_initialized"}
    
    try:
        # Get status handler from bot app
        status_handler = None
        for route in bot_app.router.routes():
            if (route.resource and 
                hasattr(route.resource, '_path') and 
                route.resource._path == '/status'):
                status_handler = route._handler
                break
        
        if status_handler:
            from aiohttp.test_utils import make_mocked_request
            mock_request = make_mocked_request('GET', '/status')
            response = await status_handler(mock_request)
            return response.body if hasattr(response, 'body') else {"status": "unknown"}
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return {"status": "error", "error": str(e)}
    
    return {"status": "handler_not_found"}

# For Azure App Service
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )