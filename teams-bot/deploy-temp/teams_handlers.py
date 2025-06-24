import structlog
from typing import Optional, Dict, Any
from botbuilder.core import TurnContext, ActivityHandler, MessageFactory
from botbuilder.schema import Activity, ActivityTypes, ChannelAccount
from teams_ai import Application, ApplicationOptions, TurnState
from teams_ai.state import MemoryStorage

from optimaize_client import get_optimaize_response
from auth_middleware import require_altura_access, AlturaAuthMiddleware
from config import config

logger = structlog.get_logger(__name__)

class OptimAIzeTeamsBot(ActivityHandler):
    """
    Main Teams bot handler for OptimAIze integration
    """
    
    def __init__(self):
        super().__init__()
        self.auth_middleware = AlturaAuthMiddleware()
        self.conversation_storage = {}  # Simple in-memory storage for conversation history
        
        logger.info("OptimAIze Teams Bot initialized")
    
    async def on_message_activity(self, turn_context: TurnContext) -> None:
        """
        Handle incoming messages from Teams users
        """
        try:
            # Check user authorization
            is_authorized, user_email = await require_altura_access(turn_context)
            
            if not is_authorized:
                await self.auth_middleware.handle_unauthorized_user(turn_context)
                return
            
            # Get user query
            user_query = turn_context.activity.text.strip()
            user_id = turn_context.activity.from_property.id
            conversation_id = turn_context.activity.conversation.id
            
            # Skip empty messages
            if not user_query:
                return
            
            # Handle special commands
            if user_query.lower() in ['/help', 'help', '?']:
                await self._send_help_message(turn_context, user_email)
                return
            
            if user_query.lower() in ['/status', 'status']:
                await self._send_status_message(turn_context, user_email)
                return
            
            # Show typing indicator
            if config.enable_typing_indicator:
                await self._send_typing_indicator(turn_context)
            
            # Log the query
            logger.info(
                "Processing user query",
                user_email=user_email,
                query_length=len(user_query),
                conversation_id=conversation_id
            )
            
            # Get conversation context
            context = self._get_conversation_context(turn_context)
            
            # Call OptimAIze backend
            response = await get_optimaize_response(
                query=user_query,
                user_id=user_id,
                user_email=user_email,
                conversation_id=conversation_id,
                context=context
            )
            
            # Send response to user
            if "error" in response:
                await self._send_error_message(turn_context, response["error"])
            else:
                await self._send_success_response(turn_context, response, user_email)
            
            # Store conversation history
            self._store_conversation_turn(conversation_id, user_query, response.get("answer", ""))
            
        except Exception as e:
            logger.error("Error processing message", error=str(e), user_email=user_email)
            await self._send_error_message(turn_context, "An unexpected error occurred. Please try again.")
    
    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ) -> None:
        """
        Handle new members being added to the conversation
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                # Check if user is authorized before sending welcome
                is_authorized, user_email = await require_altura_access(turn_context)
                
                if is_authorized:
                    await self._send_welcome_message(turn_context, user_email)
                else:
                    await self.auth_middleware.handle_unauthorized_user(turn_context)
    
    async def _send_welcome_message(self, turn_context: TurnContext, user_email: str) -> None:
        """Send welcome message to new users"""
        welcome_text = (
            f"🤖 **Welcome to OptimAIze!**\n\n"
            f"Hello {user_email.split('@')[0]}! I'm your AI assistant for searching through Altura's documents.\n\n"
            f"**What I can do:**\n"
            f"• Answer questions about company documents\n"
            f"• Search through engineering specifications\n"
            f"• Find relevant policies and procedures\n"
            f"• Provide quick access to company knowledge\n\n"
            f"**How to use me:**\n"
            f"• Just type your question in plain English\n"
            f"• Be specific for better results\n"
            f"• Type `/help` for more commands\n\n"
            f"**Example questions:**\n"
            f"• \"What is our vacation policy?\"\n"
            f"• \"How do we handle safety protocols?\"\n"
            f"• \"What are the requirements for project X?\"\n\n"
            f"Ready to help! What would you like to know? 🚀"
        )
        
        await turn_context.send_activity(MessageFactory.text(welcome_text))
        logger.info("Sent welcome message", user_email=user_email)
    
    async def _send_help_message(self, turn_context: TurnContext, user_email: str) -> None:
        """Send help information"""
        help_text = (
            f"🆘 **OptimAIze Help**\n\n"
            f"**Available Commands:**\n"
            f"• `/help` or `help` - Show this help message\n"
            f"• `/status` - Check system status\n\n"
            f"**Tips for better results:**\n"
            f"• Be specific in your questions\n"
            f"• Include relevant keywords\n"
            f"• Ask follow-up questions for clarification\n\n"
            f"**Examples:**\n"
            f"• \"What is the process for submitting expense reports?\"\n"
            f"• \"Tell me about our remote work policy\"\n"
            f"• \"How do I request time off?\"\n\n"
            f"Need more help? Contact IT support or check the admin dashboard."
        )
        
        await turn_context.send_activity(MessageFactory.text(help_text))
        logger.info("Sent help message", user_email=user_email)
    
    async def _send_status_message(self, turn_context: TurnContext, user_email: str) -> None:
        """Send system status information"""
        try:
            # Check backend health
            from optimaize_client import OptimAIzeClient
            async with OptimAIzeClient() as client:
                is_healthy = await client.health_check()
            
            status_icon = "✅" if is_healthy else "❌"
            backend_status = "Online" if is_healthy else "Offline"
            
            status_text = (
                f"📊 **OptimAIze System Status**\n\n"
                f"{status_icon} **Backend Service:** {backend_status}\n"
                f"🤖 **Bot Service:** Online\n"
                f"🔍 **Search Engine:** {backend_status}\n"
                f"🧠 **AI Model:** {backend_status}\n\n"
                f"**Your Access:**\n"
                f"✅ **Email:** {user_email}\n"
                f"✅ **Authorization:** Verified\n\n"
                f"Last updated: {self._get_current_time()}"
            )
            
            await turn_context.send_activity(MessageFactory.text(status_text))
            logger.info("Sent status message", user_email=user_email, backend_healthy=is_healthy)
            
        except Exception as e:
            logger.error("Error checking status", error=str(e))
            error_text = (
                f"❌ **System Status Check Failed**\n\n"
                f"Unable to retrieve current system status. Please try again later."
            )
            await turn_context.send_activity(MessageFactory.text(error_text))
    
    async def _send_success_response(
        self, 
        turn_context: TurnContext, 
        response: Dict[str, Any], 
        user_email: str
    ) -> None:
        """Send successful response from OptimAIze backend"""
        answer = response.get("answer", "No answer available")
        
        # Add basic formatting
        formatted_response = f"🤖 **OptimAIze Response:**\n\n{answer}"
        
        # Add metadata if available
        if "sources" in response and response["sources"]:
            formatted_response += f"\n\n📚 **Sources:** {len(response['sources'])} documents referenced"
        
        if "processing_time" in response:
            formatted_response += f"\n⏱️ *Processed in {response['processing_time']:.2f}s*"
        
        await turn_context.send_activity(MessageFactory.text(formatted_response))
        
        logger.info(
            "Sent successful response",
            user_email=user_email,
            response_length=len(answer),
            sources_count=len(response.get("sources", []))
        )
    
    async def _send_error_message(self, turn_context: TurnContext, error_message: str) -> None:
        """Send error message to user"""
        error_text = (
            f"❌ **Sorry, something went wrong**\n\n"
            f"{error_message}\n\n"
            f"**You can try:**\n"
            f"• Rephrasing your question\n"
            f"• Asking a simpler question\n"
            f"• Checking `/status` for system health\n"
            f"• Contacting IT support if the issue persists"
        )
        
        await turn_context.send_activity(MessageFactory.text(error_text))
    
    async def _send_typing_indicator(self, turn_context: TurnContext) -> None:
        """Send typing indicator to show bot is processing"""
        try:
            typing_activity = Activity(
                type=ActivityTypes.typing,
                from_property=turn_context.activity.recipient,
                recipient=turn_context.activity.from_property,
                conversation=turn_context.activity.conversation
            )
            await turn_context.send_activity(typing_activity)
        except Exception as e:
            logger.debug("Could not send typing indicator", error=str(e))
    
    def _get_conversation_context(self, turn_context: TurnContext) -> Dict[str, Any]:
        """Get additional context from Teams conversation"""
        context = {
            "conversation_type": turn_context.activity.conversation.conversation_type,
            "conversation_id": turn_context.activity.conversation.id,
            "channel_id": turn_context.activity.channel_id,
            "is_group": turn_context.activity.conversation.is_group,
        }
        
        # Add team/channel info if available
        if hasattr(turn_context.activity, 'channel_data'):
            channel_data = turn_context.activity.channel_data
            if isinstance(channel_data, dict):
                context.update({
                    "team_id": channel_data.get("team", {}).get("id"),
                    "channel_name": channel_data.get("channel", {}).get("name"),
                })
        
        return context
    
    def _store_conversation_turn(self, conversation_id: str, query: str, response: str) -> None:
        """Store conversation turn for context (simple in-memory storage)"""
        if conversation_id not in self.conversation_storage:
            self.conversation_storage[conversation_id] = []
        
        self.conversation_storage[conversation_id].append({
            "query": query,
            "response": response,
            "timestamp": self._get_current_time()
        })
        
        # Keep only the last N turns to prevent memory bloat
        max_history = config.max_conversation_history
        if len(self.conversation_storage[conversation_id]) > max_history:
            self.conversation_storage[conversation_id] = self.conversation_storage[conversation_id][-max_history:]
    
    def _get_current_time(self) -> str:
        """Get current time as formatted string"""
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")