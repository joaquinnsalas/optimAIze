"""FastAPI application for OptimAIze search and generation."""

import asyncio
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query as QueryParam
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.utils.logger import logger
from src.retrieval.search_engine import search_engine
from src.retrieval.models import SearchQuery, SearchResponse
from src.llm.processor import llm_processor
from src.llm.models import LLMQuery, LLMResponse

# FastAPI app
app = FastAPI(
    title="OptimAIze API",
    description="Production-grade RAG system with hybrid search and LLM generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    mode: str = Field(default="hybrid", description="Search mode: hybrid, semantic, keyword")
    top_k: int = Field(default=10, description="Number of results to return")
    min_similarity: float = Field(default=0.0, description="Minimum similarity threshold")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters")

class GenerateRequest(BaseModel):
    query: str = Field(..., description="User question")
    mode: str = Field(default="hybrid", description="Search mode: hybrid, semantic, keyword")
    top_k: int = Field(default=5, description="Number of chunks to retrieve")
    min_similarity: float = Field(default=0.0, description="Minimum similarity threshold")
    model: Optional[str] = Field(default=None, description="LLM model to use")
    temperature: Optional[float] = Field(default=None, description="Generation temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, Any]
    timestamp: float

class StatsResponse(BaseModel):
    documents: Dict[str, Any]
    storage: Dict[str, Any]
    search_engine: Dict[str, Any]

@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "OptimAIze API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "search": "/search",
            "generate": "/generate", 
            "health": "/health",
            "stats": "/stats",
            "docs": "/docs"
        }
    }

@app.get("/search", response_model=SearchResponse, summary="Search documents")
async def search_documents(
    q: str = QueryParam(..., description="Search query"),
    mode: str = QueryParam(default="hybrid", description="Search mode"),
    top_k: int = QueryParam(default=10, description="Number of results"),
    min_similarity: float = QueryParam(default=0.0, description="Minimum similarity")
):
    """
    Search documents using hybrid, semantic, or keyword search.
    
    - **q**: The search query
    - **mode**: Search mode (hybrid, semantic, keyword)
    - **top_k**: Maximum number of results to return
    - **min_similarity**: Minimum similarity threshold
    """
    try:
        logger.info(f"API search request: '{q}' (mode: {mode})")
        
        response = await search_engine.search(
            query=q,
            mode=mode,
            top_k=top_k,
            min_similarity=min_similarity
        )
        
        logger.info(f"API search completed: {len(response.results)} results")
        return response
        
    except Exception as e:
        logger.error(f"API search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/search", response_model=SearchResponse, summary="Search documents (POST)")
async def search_documents_post(request: SearchRequest):
    """
    Search documents using POST with request body.
    
    Allows for more complex queries and filtering options.
    """
    try:
        logger.info(f"API search POST request: '{request.query}' (mode: {request.mode})")
        
        response = await search_engine.search(
            query=request.query,
            mode=request.mode,
            top_k=request.top_k,
            min_similarity=request.min_similarity,
            filters=request.filters
        )
        
        logger.info(f"API search POST completed: {len(response.results)} results")
        return response
        
    except Exception as e:
        logger.error(f"API search POST failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/generate", response_model=LLMResponse, summary="Generate answer from query")
async def generate_answer_get(
    q: str = QueryParam(..., description="User question"),
    mode: str = QueryParam(default="hybrid", description="Search mode"),
    top_k: int = QueryParam(default=5, description="Number of chunks to retrieve"),
    min_similarity: float = QueryParam(default=0.0, description="Minimum similarity"),
    model: Optional[str] = QueryParam(default=None, description="LLM model to use"),
    temperature: Optional[float] = QueryParam(default=None, description="Generation temperature"),
    max_tokens: Optional[int] = QueryParam(default=None, description="Maximum tokens")
):
    """
    Generate an answer to a question using retrieved context and LLM.
    
    This endpoint:
    1. Searches for relevant documents using the specified mode
    2. Uses the top-k results as context for LLM generation
    3. Returns the generated answer with citations
    
    - **q**: The user's question
    - **mode**: Search mode (hybrid, semantic, keyword)  
    - **top_k**: Number of document chunks to retrieve for context
    - **min_similarity**: Minimum similarity threshold for search
    - **model**: LLM model name (overrides config default)
    - **temperature**: Generation temperature (0.0-1.0)
    - **max_tokens**: Maximum tokens to generate
    """
    try:
        logger.info(f"API generate request: '{q}' (mode: {mode}, model: {model})")
        
        llm_query = LLMQuery(
            query=q,
            mode=mode,
            top_k=top_k,
            min_similarity=min_similarity,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        response = await llm_processor.process_query(llm_query)
        
        logger.info(f"API generate completed: {len(response.llm_answer)} chars generated")
        return response
        
    except Exception as e:
        logger.error(f"API generate failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate", response_model=LLMResponse, summary="Generate answer (POST)")
async def generate_answer_post(request: GenerateRequest):
    """
    Generate an answer using POST with full request body.
    
    Provides complete control over all generation parameters.
    """
    try:
        logger.info(f"API generate POST request: '{request.query}' (mode: {request.mode})")
        
        llm_query = LLMQuery(
            query=request.query,
            mode=request.mode,
            top_k=request.top_k,
            min_similarity=request.min_similarity,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        response = await llm_processor.process_query(llm_query)
        
        logger.info(f"API generate POST completed: {len(response.llm_answer)} chars generated")
        return response
        
    except Exception as e:
        logger.error(f"API generate POST failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """
    Comprehensive health check for all system components.
    
    Checks:
    - Search engine (Qdrant + Elasticsearch)
    - LLM processor (Ollama)
    - Template system
    """
    try:
        # Check search engine health
        search_health = await search_engine.health_check()
        
        # Check LLM processor health  
        llm_health = await llm_processor.health_check()
        
        # Overall status
        overall_status = "healthy"
        if search_health.get("status") != "healthy" or llm_health.get("status") != "healthy":
            overall_status = "degraded"
        
        return HealthResponse(
            status=overall_status,
            components={
                "search_engine": search_health,
                "llm_processor": llm_health
            },
            timestamp=search_health.get("timestamp", 0)
        )
        
    except Exception as e:
        logger.error(f"API health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats", response_model=StatsResponse, summary="System statistics")
async def get_system_stats():
    """
    Get comprehensive system statistics and metrics.
    
    Returns information about:
    - Document indexing statistics
    - Storage utilization  
    - Search engine performance
    """
    try:
        from src.indexing.pipeline import indexing_pipeline
        
        # Get pipeline status
        pipeline_status = indexing_pipeline.get_pipeline_status()
        
        # Get search engine stats
        search_stats = search_engine.get_search_stats()
        
        return StatsResponse(
            documents={
                "total_files": pipeline_status.get("database_stats", {}).get("total_files", 0),
                "completed_files": pipeline_status.get("database_stats", {}).get("completed_files", 0),
                "total_chunks": pipeline_status.get("database_stats", {}).get("total_chunks", 0),
                "last_indexed": pipeline_status.get("last_update", "never")
            },
            storage={
                "qdrant_points": search_stats.get("storage", {}).get("qdrant_points", 0),
                "elasticsearch_docs": search_stats.get("storage", {}).get("elasticsearch_docs", 0)
            },
            search_engine=search_stats.get("configuration", {})
        )
        
    except Exception as e:
        logger.error(f"API stats failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

@app.get("/query-suggestions", summary="Get query suggestions")
async def get_query_suggestions(
    q: str = QueryParam(..., description="Partial query for suggestions"),
    limit: int = QueryParam(default=5, description="Maximum suggestions to return")
):
    """
    Get query suggestions based on indexed content.
    
    - **q**: Partial query text
    - **limit**: Maximum number of suggestions
    """
    try:
        # Simple implementation - could be enhanced with more sophisticated suggestion logic
        logger.info(f"API query suggestions request: '{q}'")
        
        # For now, return some common query patterns
        # In a production system, this could analyze indexed content for suggestions
        suggestions = [
            f"{q} policy",
            f"{q} procedure", 
            f"{q} benefits",
            f"{q} requirements",
            f"how to {q}"
        ]
        
        return {
            "query": q,
            "suggestions": suggestions[:limit]
        }
        
    except Exception as e:
        logger.error(f"API query suggestions failed: {e}")
        raise HTTPException(status_code=500, detail=f"Suggestions failed: {str(e)}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled API error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/search",
                "/health", 
                "/stats",
                "/query-suggestions"
            ]
        }
    )

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "message": "Invalid request parameters",
            "details": exc.errors() if hasattr(exc, "errors") else str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)