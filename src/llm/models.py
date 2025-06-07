"""Data models for LLM processing."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.retrieval.models import SearchResult

class LLMQuery(BaseModel):
    """Input query for LLM generation."""
    query: str = Field(..., description="User's question or query")
    mode: str = Field(default="hybrid", description="Search mode: hybrid, semantic, keyword")
    top_k: int = Field(default=5, description="Number of chunks to retrieve")
    min_similarity: float = Field(default=0.0, description="Minimum similarity threshold")
    model: Optional[str] = Field(default=None, description="LLM model to use (overrides config)")
    temperature: Optional[float] = Field(default=None, description="Generation temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")

class CitationSource(BaseModel):
    """Source information for citations."""
    file_name: str = Field(..., description="Source file name")
    file_path: str = Field(..., description="Full file path")
    chunk_index: int = Field(..., description="Chunk number within the file")
    page_number: Optional[int] = Field(default=None, description="Page number if available")
    content_preview: str = Field(..., description="Preview of the relevant content")
    score: float = Field(..., description="Relevance score")
    source_type: str = Field(..., description="Source of the match (semantic/keyword/hybrid)")

class LLMResponse(BaseModel):
    """Response from LLM generation."""
    query: str = Field(..., description="Original user query")
    llm_answer: str = Field(..., description="Generated answer from LLM")
    sources: List[CitationSource] = Field(default_factory=list, description="Citation sources")
    search_results: List[SearchResult] = Field(default_factory=list, description="Original search results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Generation metadata")
    
    class Config:
        json_encoders = {
            # Handle any special encoding if needed
        }

class LLMGenerationMetadata(BaseModel):
    """Metadata about the LLM generation process."""
    model: str = Field(..., description="LLM model used")
    search_time_ms: float = Field(..., description="Time spent on retrieval")
    generation_time_ms: float = Field(..., description="Time spent on LLM generation")
    total_time_ms: float = Field(..., description="Total processing time")
    search_mode: str = Field(..., description="Search mode used")
    chunks_used: int = Field(..., description="Number of chunks provided to LLM")
    chunks_cited: int = Field(..., description="Number of chunks actually cited")
    ollama_available: bool = Field(..., description="Whether Ollama was available")
    generation_params: Dict[str, Any] = Field(default_factory=dict, description="LLM generation parameters")

class OllamaRequest(BaseModel):
    """Request format for Ollama API."""
    model: str = Field(..., description="Model name")
    prompt: str = Field(..., description="Complete prompt")
    stream: bool = Field(default=False, description="Whether to stream response")
    options: Dict[str, Any] = Field(default_factory=dict, description="Generation options")

class OllamaResponse(BaseModel):
    """Response format from Ollama API."""
    model: str = Field(..., description="Model used")
    response: str = Field(..., description="Generated text")
    done: bool = Field(..., description="Whether generation is complete")
    total_duration: Optional[int] = Field(default=None, description="Total time in nanoseconds")
    load_duration: Optional[int] = Field(default=None, description="Model load time")
    prompt_eval_count: Optional[int] = Field(default=None, description="Prompt tokens")
    prompt_eval_duration: Optional[int] = Field(default=None, description="Prompt evaluation time")
    eval_count: Optional[int] = Field(default=None, description="Generated tokens")
    eval_duration: Optional[int] = Field(default=None, description="Generation time")

class LLMError(BaseModel):
    """Error information for LLM failures."""
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error description")
    fallback_used: bool = Field(default=False, description="Whether fallback was triggered")
    search_results_available: bool = Field(default=False, description="Whether search results are available")