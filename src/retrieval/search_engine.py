"""Main search engine for OptimAIze hybrid retrieval."""

import asyncio
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.config.settings import config
from src.utils.logger import logger
from src.storage.qdrant_client import qdrant_manager
from src.storage.elasticsearch_client import elasticsearch_manager
from src.indexing.embedder import TextEmbedder
from src.retrieval.models import SearchResult, SearchQuery, SearchResponse
from src.retrieval.query_processor import QueryProcessor
from src.retrieval.fusion import ResultFusion

class SearchEngine:
    """Main search engine that coordinates hybrid retrieval."""
    
    def __init__(self):
        self.retrieval_config = config.retrieval
        self.embedder = TextEmbedder()
        self.query_processor = QueryProcessor()
        self.fusion_engine = ResultFusion()
        
        # Search configuration
        self.top_k_per_source = self.retrieval_config.get("top_k_per_source", 20)
        self.concurrent_search = self.retrieval_config.get("concurrent_search", True)
        self.search_timeout = self.retrieval_config.get("search_timeout", 30.0)
        
        logger.info("Search engine initialized")
    
    async def search(self, query: str, mode: str = "hybrid", 
                    top_k: int = None, min_similarity: float = None,
                    filters: Dict[str, Any] = None) -> SearchResponse:
        """Perform search with specified mode."""
        start_time = time.time()
        
        try:
            # Process the query
            search_query = self.query_processor.process_query(
                query, mode, top_k, min_similarity, filters
            )
            
            logger.info(f"Executing {search_query.mode} search for: '{search_query.processed_query}'")
            
            # Execute search based on mode
            if search_query.mode == "semantic":
                results, sources = await self._semantic_search_only(search_query)
                fusion_info = None
            elif search_query.mode == "keyword":
                results, sources = await self._keyword_search_only(search_query)
                fusion_info = None
            else:  # hybrid
                results, sources, fusion_info = await self._hybrid_search(search_query)
            
            # Calculate search time
            search_time_ms = (time.time() - start_time) * 1000
            
            # Create response
            response = SearchResponse(
                query=search_query.raw_query,
                mode=search_query.mode,
                results=results,
                total_found=len(results),
                search_time_ms=search_time_ms,
                sources_searched=sources,
                fusion_method=fusion_info.get("method") if fusion_info else None,
                fusion_params=fusion_info
            )
            
            logger.info(f"Search completed: {len(results)} results in {search_time_ms:.1f}ms")
            return response
        
        except Exception as e:
            logger.error(f"Search failed: {e}")
            # Return empty response with error info
            search_time_ms = (time.time() - start_time) * 1000
            return SearchResponse(
                query=query,
                mode=mode,
                results=[],
                total_found=0,
                search_time_ms=search_time_ms,
                sources_searched=[],
                fusion_method=None,
                fusion_params={"error": str(e)}
            )
    
    async def _hybrid_search(self, search_query: SearchQuery) -> tuple[List[SearchResult], List[str], Dict[str, Any]]:
        """Perform hybrid search combining semantic and keyword results."""
        
        if self.concurrent_search:
            # Run searches concurrently
            semantic_task = asyncio.create_task(self._get_semantic_results(search_query))
            keyword_task = asyncio.create_task(self._get_keyword_results(search_query))
            
            try:
                semantic_results, keyword_results = await asyncio.wait_for(
                    asyncio.gather(semantic_task, keyword_task),
                    timeout=self.search_timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Search timeout after {self.search_timeout}s")
                semantic_results, keyword_results = [], []
        else:
            # Run searches sequentially
            semantic_results = await self._get_semantic_results(search_query)
            keyword_results = await self._get_keyword_results(search_query)
        
        # Fuse results
        fused_results, fusion_info = self.fusion_engine.fuse_results(
            semantic_results, keyword_results, search_query.top_k
        )
        
        return fused_results, ["qdrant", "elasticsearch"], fusion_info
    
    async def _semantic_search_only(self, search_query: SearchQuery) -> tuple[List[SearchResult], List[str]]:
        """Perform semantic search only."""
        results = await self._get_semantic_results(search_query)
        return results[:search_query.top_k], ["qdrant"]
    
    async def _keyword_search_only(self, search_query: SearchQuery) -> tuple[List[SearchResult], List[str]]:
        """Perform keyword search only."""
        results = await self._get_keyword_results(search_query)
        return results[:search_query.top_k], ["elasticsearch"]
    
    async def _get_semantic_results(self, search_query: SearchQuery) -> List[SearchResult]:
        """Get results from semantic search (Qdrant)."""
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed_text(search_query.processed_query)
            
            # Search Qdrant
            qdrant_results = qdrant_manager.search_similar(
                query_embedding=query_embedding,
                limit=self.top_k_per_source,
                score_threshold=search_query.min_similarity,
                filter_conditions=search_query.filters
            )
            
            # Convert to SearchResult objects
            results = []
            for result in qdrant_results:
                search_result = self._convert_qdrant_result(result)
                if search_result:
                    results.append(search_result)
            
            logger.debug(f"Found {len(results)} semantic results")
            return results
        
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
    
    async def _get_keyword_results(self, search_query: SearchQuery) -> List[SearchResult]:
        """Get results from keyword search (Elasticsearch)."""
        try:
            # Build filters for Elasticsearch
            es_filters = self._build_elasticsearch_filters(search_query.filters)
            
            # Search Elasticsearch
            es_results = elasticsearch_manager.search_keywords(
                query=search_query.processed_query,
                limit=self.top_k_per_source,
                filters=es_filters
            )
            
            # Convert to SearchResult objects
            results = []
            for result in es_results:
                search_result = self._convert_elasticsearch_result(result)
                if search_result:
                    results.append(search_result)
            
            logger.debug(f"Found {len(results)} keyword results")
            return results
        
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def _convert_qdrant_result(self, qdrant_result: Dict[str, Any]) -> Optional[SearchResult]:
        """Convert Qdrant result to SearchResult object."""
        try:
            metadata = qdrant_result.get("metadata", {})
            
            return SearchResult(
                content=qdrant_result.get("content", ""),
                chunk_id=qdrant_result.get("chunk_id", ""),
                file_path=metadata.get("source", ""),
                file_name=Path(metadata.get("source", "")).name,
                chunk_index=metadata.get("chunk_index", 0),
                score=qdrant_result.get("score", 0.0),
                source_type="semantic",
                page_number=metadata.get("page_number"),
                file_type=metadata.get("type"),
                total_chunks=metadata.get("total_chunks")
            )
        except Exception as e:
            logger.error(f"Error converting Qdrant result: {e}")
            return None
    
    def _convert_elasticsearch_result(self, es_result: Dict[str, Any]) -> Optional[SearchResult]:
        """Convert Elasticsearch result to SearchResult object."""
        try:
            metadata = es_result.get("metadata", {})
            
            # Extract highlights if available
            highlights = es_result.get("highlights", [])
            
            return SearchResult(
                content=es_result.get("content", ""),
                chunk_id=es_result.get("chunk_id", ""),
                file_path=metadata.get("source", ""),
                file_name=Path(metadata.get("source", "")).name,
                chunk_index=metadata.get("chunk_index", 0),
                score=es_result.get("score", 0.0),
                source_type="keyword",
                page_number=metadata.get("page_number"),
                highlights=highlights if highlights else None,
                file_type=metadata.get("type"),
                total_chunks=metadata.get("total_chunks")
            )
        except Exception as e:
            logger.error(f"Error converting Elasticsearch result: {e}")
            return None
    
    def _build_elasticsearch_filters(self, filters: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Build Elasticsearch filters from query filters."""
        if not filters:
            return None
        
        es_filters = {}
        
        # Map common filter fields
        if "type" in filters:
            es_filters["type"] = filters["type"]
        
        if "source" in filters:
            es_filters["source"] = filters["source"]
        
        return es_filters if es_filters else None
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search engine statistics and health."""
        try:
            # Get component health
            qdrant_healthy = qdrant_manager.health_check()
            es_healthy = elasticsearch_manager.health_check()
            
            # Get collection/index info
            qdrant_info = qdrant_manager.get_collection_info()
            es_info = elasticsearch_manager.get_index_stats()
            
            return {
                "health": {
                    "qdrant": qdrant_healthy,
                    "elasticsearch": es_healthy,
                    "embedder": True,  # Assume healthy if no exception
                    "overall": qdrant_healthy and es_healthy
                },
                "storage": {
                    "qdrant_points": qdrant_info.get("points_count", 0),
                    "elasticsearch_docs": es_info.get("document_count", 0)
                },
                "configuration": {
                    "top_k_per_source": self.top_k_per_source,
                    "concurrent_search": self.concurrent_search,
                    "fusion_method": self.fusion_engine.fusion_method,
                    "embedding_model": self.embedder.model_name
                }
            }
        except Exception as e:
            logger.error(f"Error getting search stats: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        try:
            # Test a simple search
            test_query = "test"
            start_time = time.time()
            
            response = await self.search(test_query, mode="hybrid", top_k=1)
            
            search_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy" if response.total_found >= 0 else "unhealthy",
                "test_search_time_ms": search_time,
                "components": self.get_search_stats()["health"],
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

# Global search engine instance
search_engine = SearchEngine()