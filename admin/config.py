"""Configuration for admin portal."""

import os
from pathlib import Path

class AdminConfig:
    """Admin portal configuration."""
    
    # Database
    DATABASE_URL = os.getenv("ADMIN_DATABASE_URL", "sqlite:///./data/admin.db")
    
    # Security
    SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "optimaize-admin-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ADMIN_TOKEN_EXPIRE_MINUTES", "480"))  # 8 hours
    
    # Paths
    BASE_DIR = Path(__file__).parent
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATES_DIR = BASE_DIR / "templates"
    
    # External services
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    MAIN_API_URL = os.getenv("MAIN_API_URL", "http://localhost:8000")
    
    # Features
    ENABLE_REGISTRATION = os.getenv("ADMIN_ENABLE_REGISTRATION", "false").lower() == "true"
    LOG_RETENTION_DAYS = int(os.getenv("ADMIN_LOG_RETENTION_DAYS", "90"))
    
    # Development
    DEBUG = os.getenv("ADMIN_DEBUG", "false").lower() == "true"
    RELOAD = os.getenv("ADMIN_RELOAD", "true").lower() == "true"

config = AdminConfig()