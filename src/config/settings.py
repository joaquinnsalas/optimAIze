"""Configuration management for OptimAIze."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration manager for OptimAIze."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._apply_env_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides."""
        # Qdrant URL override
        if qdrant_url := os.getenv("QDRANT_URL"):
            self._config["qdrant"]["url"] = qdrant_url
        
        # Elasticsearch URL override
        if es_url := os.getenv("ELASTICSEARCH_URL"):
            self._config["elasticsearch"]["url"] = es_url
        
        # Database overrides
        if db_type := os.getenv("DATABASE_TYPE"):
            self._config["database"]["type"] = db_type
        
        if pg_url := os.getenv("POSTGRESQL_URL"):
            self._config["database"]["postgresql_url"] = pg_url
        
        # Embedding device override
        if device := os.getenv("EMBEDDING_DEVICE"):
            self._config["embeddings"]["device"] = device
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation (e.g., 'app.name')."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @property
    def app(self) -> Dict[str, Any]:
        return self._config.get("app", {})
    
    @property
    def indexing(self) -> Dict[str, Any]:
        return self._config.get("indexing", {})
    
    @property
    def embeddings(self) -> Dict[str, Any]:
        return self._config.get("embeddings", {})
    
    @property
    def qdrant(self) -> Dict[str, Any]:
        return self._config.get("qdrant", {})
    
    @property
    def elasticsearch(self) -> Dict[str, Any]:
        return self._config.get("elasticsearch", {})
    
    @property
    def database(self) -> Dict[str, Any]:
        return self._config.get("database", {})
    
    @property
    def logging(self) -> Dict[str, Any]:
        return self._config.get("logging", {})
    
    @property
    def retrieval(self) -> Dict[str, Any]:
        return self._config.get("retrieval", {})

# Global config instance
config = Config()