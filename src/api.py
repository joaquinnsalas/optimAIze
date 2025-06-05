from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from contextlib import asynccontextmanager

from search import HybridSearcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global searcher instance
searcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global searcher
    try:
        logger.info("🚀 Starting OptimAIze Search API...")
        searcher = HybridSearcher()
        logger.info("✅ Search system initialized")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        raise
    finally:
        if searcher:
            searcher.close()
            logger.info("🔌 Search system closed")

# Initialize FastAPI
app = FastAPI(
    title="OptimAIze Search API",
    description="Hybrid semantic + keyword search for your documents",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    
class SearchResult(BaseModel):
    chunk_id: str
    chunk_text: str
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    document_id: Optional[str] = None
    combined_score: float
    semantic_score: Optional[float] = None
    keyword_score: Optional[float] = None
    source: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResult]
    
class DocumentInfoResponse(BaseModel):
    document_id: str
    file_name: str
    file_path: str
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    last_modified: Optional[float] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is healthy"""
    try:
        if searcher is None:
            raise HTTPException(status_code=503, detail="Search system not initialized")
        return {"status": "healthy", "message": "OptimAIze Search API is running"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Main search endpoint
@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Search documents using hybrid semantic + keyword search
    """
    try:
        if searcher is None:
            raise HTTPException(status_code=503, detail="Search system not initialized")
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if request.top_k < 1 or request.top_k > 100:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 100")
        
        logger.info(f"Search request: '{request.query}' (top_k={request.top_k})")
        
        # Perform search
        results = searcher.search(request.query, request.top_k)
        
        # Format response
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                chunk_id=result.get('chunk_id', ''),
                chunk_text=result.get('chunk_text', ''),
                file_name=result.get('file_name', ''),
                file_path=result.get('file_path', ''),
                document_id=result.get('document_id', ''),
                combined_score=result.get('combined_score', 0.0),
                semantic_score=result.get('semantic_score'),
                keyword_score=result.get('keyword_score'),
                source=result.get('source', '')
            ))
        
        return SearchResponse(
            query=request.query,
            total_results=len(search_results),
            results=search_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Get document info endpoint
@app.get("/document/{document_id}", response_model=DocumentInfoResponse)
async def get_document_info(document_id: str):
    """
    Get detailed information about a specific document
    """
    try:
        if searcher is None:
            raise HTTPException(status_code=503, detail="Search system not initialized")
        
        doc_info = searcher.get_document_info(document_id)
        
        if not doc_info:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentInfoResponse(**doc_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get document info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get document info: {str(e)}")

# Statistics endpoint
@app.get("/stats")
async def get_stats():
    """
    Get search system statistics
    """
    try:
        if searcher is None:
            raise HTTPException(status_code=503, detail="Search system not initialized")
        
        # Get document count
        cursor = searcher.conn.cursor()
        doc_count = cursor.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        chunk_count = cursor.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        
        # Get collection info from Qdrant
        collection_info = searcher.qdrant.get_collection(searcher.qdrant.collection_name)
        vector_count = collection_info.vectors_count
        
        return {
            "documents": doc_count,
            "chunks": chunk_count,
            "vectors": vector_count,
            "collection_name": "optimAIze-index"
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

# Simple test endpoint
@app.get("/test")
async def test_search():
    """
    Test the search with a simple query
    """
    try:
        test_results = await search_documents(SearchRequest(
            query="engineering project",
            top_k=3
        ))
        return {
            "message": "Test successful",
            "sample_results": test_results.total_results
        }
    except Exception as e:
        return {"message": f"Test failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting OptimAIze Search API...")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔍 Test search at: http://localhost:8000/test")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )