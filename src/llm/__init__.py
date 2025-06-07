"""LLM processing module for OptimAIze."""

from .processor import llm_processor, LLMProcessor
from .ollama_client import ollama_client, OllamaClient
from .models import (
    LLMQuery,
    LLMResponse, 
    CitationSource,
    LLMGenerationMetadata,
    OllamaRequest,
    OllamaResponse,
    LLMError
)

__all__ = [
    "llm_processor",
    "LLMProcessor",
    "ollama_client", 
    "OllamaClient",
    "LLMQuery",
    "LLMResponse",
    "CitationSource", 
    "LLMGenerationMetadata",
    "OllamaRequest",
    "OllamaResponse",
    "LLMError"
]