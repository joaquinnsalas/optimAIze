"""Configuration settings for OptimAIze."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for OptimAIze."""
    
    def __init__(self):
        # Look for config.yaml in the project root first, then in src/config
        root_config = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        local_config = Path(__file__).parent / "config.yaml"
        
        if root_config.exists():
            self.config_path = root_config
        else:
            self.config_path = local_config
            
        self._load_config()
        
        # Core settings
        self.indexing = self.config.get("indexing", {})
        self.embeddings = self.config.get("embeddings", {})
        self.retrieval = self.config.get("retrieval", {})
        self.qdrant = self.config.get("qdrant", {})
        self.elasticsearch = self.config.get("elasticsearch", {})
        self.api = self.config.get("api", {})
        self.llm = self.config.get("llm", {})  # Add LLM config
        self.database = self.config.get("database", {})  # Add database config
        self.logging = self.config.get("logging", {})  # Add logging config
        
        # Validate critical settings
        self._validate_config()
    
    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
    
    def _validate_config(self):
        """Validate configuration settings."""
        # Check required sections
        required_sections = ["indexing", "embeddings", "retrieval", "qdrant", "elasticsearch"]
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")
        
        # Validate embeddings model
        if not self.embeddings.get("model_name"):
            raise ValueError("Embeddings model_name is required")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with optional default."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def update_from_env(self):
        """Update configuration from environment variables."""
        # Qdrant URL
        if os.getenv("QDRANT_URL"):
            self.qdrant["url"] = os.getenv("QDRANT_URL")
        
        # Elasticsearch URL
        if os.getenv("ELASTICSEARCH_URL"):
            self.elasticsearch["url"] = os.getenv("ELASTICSEARCH_URL")
        
        # API settings
        if os.getenv("API_HOST"):
            self.api["host"] = os.getenv("API_HOST")
        if os.getenv("API_PORT"):
            self.api["port"] = int(os.getenv("API_PORT"))
        
        # LLM settings
        if os.getenv("OLLAMA_URL"):
            self.llm["ollama_url"] = os.getenv("OLLAMA_URL")
        if os.getenv("LLM_MODEL"):
            self.llm["default_model"] = os.getenv("LLM_MODEL")
        
        # Embedding device
        if os.getenv("EMBEDDING_DEVICE"):
            self.embeddings["device"] = os.getenv("EMBEDDING_DEVICE")
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return {
            "indexing": self.indexing,
            "embeddings": self.embeddings,
            "retrieval": self.retrieval,
            "qdrant": self.qdrant,
            "elasticsearch": self.elasticsearch,
            "api": self.api,
            "llm": self.llm,
            "database": self.database,
            "logging": self.logging
        }

# Global configuration instance
config = Config()

# Update from environment variables
config.update_from_env()