# FastAPI REST endpoints
"""REST API for OptimAIze search functionality."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import asyncio
from src.retrieval.search_engine import search_engine
from src.utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="OptimAIze Search API",
    description="Production-grade RAG system with hybrid search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "OptimAIze Search API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "health": "/health",
            "stats": "/stats"
        }
    }

@app.get("/search")
async def search_documents(
    q: str = Query(..., description="Search query", min_length=1),
    mode: str = Query("hybrid", description="Search mode: hybrid, semantic, or keyword"),
    top_k: Optional[int] = Query(10, description="Number of results to return", ge=1, le=100),
    min_similarity: Optional[float] = Query(0.0, description="Minimum similarity threshold", ge=0.0, le=1.0),
    filetype: Optional[str] = Query(None, description="Filter by file type (pdf, docx, etc.)"),
    source: Optional[str] = Query(None, description="Filter by source file path")
):
    """
    Search documents using hybrid, semantic, or keyword search.
    
    Parameters:
    - q: The search query (required)
    - mode: Search mode - "hybrid" (default), "semantic", or "keyword"
    - top_k: Number of results to return (1-100, default: 10)
    - min_similarity: Minimum similarity threshold for semantic search (0.0-1.0)
    - filetype: Filter results by file type (optional)
    - source: Filter results by source file (optional)
    
    Returns:
    - JSON response with search results and metadata
    """
    try:
        # Validate search mode
        if mode.lower() not in ["hybrid", "semantic", "keyword"]:
            raise HTTPException(
                status_code=400, 
                detail="Invalid search mode. Must be 'hybrid', 'semantic', or 'keyword'"
            )
        
        # Build filters
        filters = {}
        if filetype:
            filters["type"] = filetype.lower()
        if source:
            filters["source"] = source
        
        # Perform search
        response = await search_engine.search(
            query=q,
            mode=mode.lower(),
            top_k=top_k,
            min_similarity=min_similarity,
            filters=filters if filters else None
        )
        
        return response.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search API error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Comprehensive health check for the search system.
    
    Returns:
    - System health status and component information
    """
    try:
        health_info = await search_engine.health_check()
        
        # Return appropriate HTTP status
        if health_info.get("status") == "healthy":
            return health_info
        else:
            raise HTTPException(status_code=503, detail=health_info)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats")
async def get_search_stats():
    """
    Get search engine statistics and configuration.
    
    Returns:
    - Search engine statistics, health, and configuration info
    """
    try:
        stats = search_engine.get_search_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/query-suggestions")
async def get_query_suggestions(
    q: str = Query(..., description="Query to analyze", min_length=1)
):
    """
    Get suggestions for improving search queries.
    
    Parameters:
    - q: The query to analyze
    
    Returns:
    - Query analysis and improvement suggestions
    """
    try:
        suggestions = search_engine.query_processor.suggest_query_improvements(q)
        stats = search_engine.query_processor.get_query_stats(q)
        
        return {
            "query": q,
            "suggestions": suggestions,
            "stats": stats
        }
    
    except Exception as e:
        logger.error(f"Query suggestions error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze query: {str(e)}")

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