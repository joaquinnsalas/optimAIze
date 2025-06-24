import os
from typing import Optional
from pydantic_settings import BaseSettings

class BotConfig(BaseSettings):
    """Configuration for the OptimAIze Teams Bot"""
    
    # Azure Bot Service Configuration
    app_id: str = os.getenv("MICROSOFT_APP_ID", "")
    app_password: str = os.getenv("MICROSOFT_APP_PASSWORD", "")
    app_tenant_id: str = os.getenv("MICROSOFT_APP_TENANT_ID", "")
    app_type: str = os.getenv("MICROSOFT_APP_TYPE", "UserAssignedMSI")
    
    # OptimAIze Backend Configuration
    optimaize_backend_url: str = os.getenv("OPTIMAIZE_BACKEND_URL", "https://your-optimaize-backend.azurewebsites.net")
    optimaize_api_timeout: int = int(os.getenv("OPTIMAIZE_API_TIMEOUT", "30"))
    
    # Altura Tenant Configuration
    altura_tenant_id: str = os.getenv("ALTURA_TENANT_ID", "")
    altura_domain: str = os.getenv("ALTURA_DOMAIN", "alturaengineering.com")
    
    # Bot Behavior Settings
    max_conversation_history: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    enable_typing_indicator: bool = os.getenv("ENABLE_TYPING_INDICATOR", "true").lower() == "true"
    bot_welcome_message: str = os.getenv("BOT_WELCOME_MESSAGE", 
        "👋 Hello! I'm the OptimAIze assistant. Ask me anything about your company documents!")
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    enable_analytics_logging: bool = os.getenv("ENABLE_ANALYTICS_LOGGING", "true").lower() == "true"
    
    # Azure Environment
    azure_tenant_id: str = os.getenv("AZURE_TENANT_ID", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global config instance
config = BotConfig()

# Validation
def validate_config():
    """Validate that all required configuration is present"""
    required_fields = [
        ("MICROSOFT_APP_ID", config.app_id),
        ("OPTIMAIZE_BACKEND_URL", config.optimaize_backend_url),
        ("ALTURA_TENANT_ID", config.altura_tenant_id),
    ]
    
    missing_fields = []
    for field_name, field_value in required_fields:
        if not field_value:
            missing_fields.append(field_name)
    
    if missing_fields:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")
    
    return True