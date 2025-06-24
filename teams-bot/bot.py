"""
OptimAIze Teams Bot - Main Bot Application

This is the main entry point for the OptimAIze Teams Bot that integrates
with the existing OptimAIze FastAPI backend.
"""

import structlog
import asyncio
from typing import Dict, Any
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
    MemoryStorage,
    ConversationState,
    UserState
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from teams_handlers import OptimAIzeTeamsBot
from config import config, validate_config
from optimaize_client import OptimAIzeClient

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

class OptimAIzeBotApp:
    """Main application class for the OptimAIze Teams Bot"""
    
    def __init__(self):
        self.bot = None
        self.adapter = None
        self.app = None
        
    async def initialize(self):
        """Initialize the bot application"""
        try:
            # Validate configuration
            validate_config()
            logger.info("Configuration validated successfully")
            
            # Create Bot Framework Adapter
            settings = BotFrameworkAdapterSettings(
                app_id=config.app_id,
                app_password=config.app_password,
                app_type=config.app_type,
                app_tenant_id=config.app_tenant_id
            )
            
            self.adapter = BotFrameworkAdapter(settings)
            
            # Add error handler to adapter
            async def on_error(context: TurnContext, error: Exception):
                logger.error(f"Error in bot adapter: {error}")
                await context.send_activity("Sorry, it looks like something went wrong.")
            
            self.adapter.on_turn_error = on_error
            
            # Create the bot
            self.bot = OptimAIzeTeamsBot()
            
            # Test backend connectivity
            await self._test_backend_connectivity()
            
            logger.info("OptimAIze Teams Bot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise
    
    async def _test_backend_connectivity(self):
        """Test connectivity to OptimAIze backend"""
        try:
            async with OptimAIzeClient() as client:
                is_healthy = await client.health_check()
                if is_healthy:
                    logger.info("Successfully connected to OptimAIze backend")
                else:
                    logger.warning("OptimAIze backend health check failed")
        except Exception as e:
            logger.error(f"Failed to connect to OptimAIze backend: {e}")
    
    def create_app(self) -> web.Application:
        """Create and configure the aiohttp web application"""
        app = web.Application(middlewares=[aiohttp_error_middleware])
        
        # Add bot message endpoint
        app.router.add_post("/api/messages", self.messages_handler)
        
        # Add health check endpoint
        app.router.add_get("/health", self.health_handler)
        app.router.add_get("/", self.health_handler)  # Root endpoint
        
        # Add status endpoint
        app.router.add_get("/status", self.status_handler)
        
        self.app = app
        return app
    
    async def messages_handler(self, req: Request) -> Response:
        """Handle incoming messages from Teams"""
        try:
            # Validate request format
            if "application/json" in req.headers.get("Content-Type", ""):
                body = await req.json()
            else:
                logger.warning("Received non-JSON request")
                return Response(status=400, text="Request must be JSON")
            
            # Create activity from request
            activity = Activity().deserialize(body)
            
            # Process the activity
            auth_header = req.headers.get("Authorization", "")
            response = await self.adapter.process_activity(activity, auth_header, self.bot.on_message_activity)
            
            if response:
                return json_response(data=response.body, status=response.status)
            
            return Response(status=200)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return Response(status=500, text=f"Error processing message: {str(e)}")
    
    async def health_handler(self, req: Request) -> Response:
        """Health check endpoint"""
        try:
            # Check backend health
            async with OptimAIzeClient() as client:
                backend_healthy = await client.health_check()
            
            health_status = {
                "status": "healthy" if backend_healthy else "degraded",
                "bot_service": "online",
                "optimaize_backend": "online" if backend_healthy else "offline",
                "timestamp": self._get_current_timestamp()
            }
            
            status_code = 200 if backend_healthy else 503
            return json_response(health_status, status=status_code)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return json_response({
                "status": "error",
                "error": str(e),
                "timestamp": self._get_current_timestamp()
            }, status=500)
    
    async def status_handler(self, req: Request) -> Response:
        """Detailed status endpoint"""
        try:
            # Get detailed status information
            async with OptimAIzeClient() as client:
                backend_healthy = await client.health_check()
            
            status_info = {
                "service": "OptimAIze Teams Bot",
                "version": "1.0.0",
                "status": "running",
                "components": {
                    "bot_framework": "online",
                    "optimaize_backend": {
                        "status": "online" if backend_healthy else "offline",
                        "url": config.optimaize_backend_url
                    },
                    "authentication": "configured",
                    "altura_tenant": config.altura_tenant_id[:8] + "..." if config.altura_tenant_id else "not_configured"
                },
                "configuration": {
                    "typing_indicator": config.enable_typing_indicator,
                    "analytics_logging": config.enable_analytics_logging,
                    "max_conversation_history": config.max_conversation_history
                },
                "timestamp": self._get_current_timestamp()
            }
            
            return json_response(status_info)
            
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return json_response({
                "status": "error",
                "error": str(e)
            }, status=500)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

# Global bot application instance
bot_app = OptimAIzeBotApp()

async def init_bot_app() -> web.Application:
    """Initialize and return the bot application"""
    await bot_app.initialize()
    return bot_app.create_app()

def main():
    """Main entry point for running the bot locally"""
    import os
    from aiohttp import web
    
    # Set up environment
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    # Configure logging level
    import logging
    logging.basicConfig(level=getattr(logging, config.log_level.upper()))
    
    async def create_app():
        return await init_bot_app()
    
    # Run the application
    web.run_app(
        create_app(),
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 3978))
    )

if __name__ == "__main__":
    main()