import structlog
from typing import Optional, Dict, Any
from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ChannelAccount
from config import config

logger = structlog.get_logger(__name__)

class AlturaAuthMiddleware:
    """Middleware to verify users are part of the Altura Microsoft 365 tenant"""
    
    def __init__(self):
        self.altura_domain = config.altura_domain
        self.altura_tenant_id = config.altura_tenant_id
    
    async def verify_user_access(self, turn_context: TurnContext) -> tuple[bool, Optional[str]]:
        """
        Verify that the user is authorized to use the bot
        
        Args:
            turn_context: The turn context from Teams
            
        Returns:
            Tuple of (is_authorized, user_email)
        """
        try:
            # Get user information from Teams context
            user_info = await self._get_user_info(turn_context)
            
            if not user_info:
                logger.warning("Could not retrieve user information from Teams context")
                return False, None
            
            user_email = user_info.get("email", "").lower()
            user_tenant_id = user_info.get("tenant_id", "")
            
            # Check if user email is from Altura domain
            is_altura_email = user_email.endswith(f"@{self.altura_domain}")
            
            # Check if user is from the correct tenant (if tenant ID is available)
            is_correct_tenant = True
            if user_tenant_id and self.altura_tenant_id:
                is_correct_tenant = user_tenant_id == self.altura_tenant_id
            
            is_authorized = is_altura_email and is_correct_tenant
            
            if is_authorized:
                logger.info(
                    "User authorized successfully",
                    user_email=user_email,
                    tenant_match=is_correct_tenant
                )
            else:
                logger.warning(
                    "User authorization failed",
                    user_email=user_email,
                    is_altura_email=is_altura_email,
                    is_correct_tenant=is_correct_tenant
                )
            
            return is_authorized, user_email if is_authorized else None
            
        except Exception as e:
            logger.error("Error during user authorization", error=str(e))
            return False, None
    
    async def _get_user_info(self, turn_context: TurnContext) -> Optional[Dict[str, Any]]:
        """
        Extract user information from Teams turn context
        
        Args:
            turn_context: The turn context from Teams
            
        Returns:
            Dict containing user information or None if not available
        """
        try:
            activity = turn_context.activity
            
            # Get basic user info from activity
            user_id = activity.from_property.id if activity.from_property else None
            user_name = activity.from_property.name if activity.from_property else None
            
            # Try to get email from different possible locations
            user_email = None
            
            # Method 1: Check if email is in the user properties
            if hasattr(activity, 'from_property') and activity.from_property:
                if hasattr(activity.from_property, 'properties'):
                    user_email = activity.from_property.properties.get('email')
                
                # Method 2: Sometimes email is in the AAD object ID format
                if not user_email and hasattr(activity.from_property, 'aad_object_id'):
                    # For now, we'll try to construct email from user name
                    # This is a fallback - in production you might want to call Graph API
                    pass
            
            # Method 3: Try to extract from channel data
            if not user_email and hasattr(activity, 'channel_data'):
                channel_data = activity.channel_data
                if isinstance(channel_data, dict):
                    tenant_info = channel_data.get('tenant', {})
                    user_email = tenant_info.get('userPrincipalName')
            
            # Method 4: If we have a user name that looks like an email
            if not user_email and user_name and '@' in user_name:
                user_email = user_name
            
            # Get tenant information
            tenant_id = None
            if hasattr(activity, 'channel_data') and isinstance(activity.channel_data, dict):
                tenant_info = activity.channel_data.get('tenant', {})
                tenant_id = tenant_info.get('id')
            
            user_info = {
                'user_id': user_id,
                'user_name': user_name,
                'email': user_email,
                'tenant_id': tenant_id
            }
            
            logger.debug("Extracted user info", user_info=user_info)
            return user_info
            
        except Exception as e:
            logger.error("Error extracting user info", error=str(e))
            return None
    
    def get_unauthorized_message(self) -> str:
        """
        Get the message to show unauthorized users
        """
        return (
            f"🚫 **Access Denied**\n\n"
            f"This bot is only available to Altura Engineering employees. "
            f"Please make sure you're signed in with your @{self.altura_domain} account.\n\n"
            f"If you believe this is an error, please contact your IT administrator."
        )
    
    async def handle_unauthorized_user(self, turn_context: TurnContext) -> None:
        """
        Handle unauthorized user by sending appropriate message
        """
        await turn_context.send_activity(self.get_unauthorized_message())
        
        # Log the unauthorized access attempt
        logger.warning(
            "Unauthorized access attempt",
            user_id=turn_context.activity.from_property.id if turn_context.activity.from_property else "unknown",
            conversation_id=turn_context.activity.conversation.id if turn_context.activity.conversation else "unknown"
        )

# Helper function to check authorization in handlers
async def require_altura_access(turn_context: TurnContext) -> tuple[bool, Optional[str]]:
    """
    Convenience function to check if user has access
    
    Returns:
        Tuple of (is_authorized, user_email)
    """
    auth_middleware = AlturaAuthMiddleware()
    return await auth_middleware.verify_user_access(turn_context)