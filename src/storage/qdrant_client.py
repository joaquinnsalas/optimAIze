"""Qdrant vector database client for OptimAIze."""

import uuid
from typing import List, Dict, Any, Optional, Union
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct, Filter, 
    FieldCondition, MatchValue, CollectionInfo
)
from src.config.settings import config
from src.utils.logger import logger

class QdrantManager:
    """Qdrant vector database manager."""
    
    def __init__(self):
        self.qdrant_config = config.qdrant
        self.client = self._initialize_client()
        self.collection_name = self.qdrant_config.get("collection_name", "optimaize_documents")
        self.vector_size = self.qdrant_config.get("vector_size", 768)
        
        # Handle distance metric with proper mapping
        distance_str = self.qdrant_config.get("distance", "COSINE").upper()
        if hasattr(Distance, distance_str):
            self.distance = getattr(Distance, distance_str)
        else:
            logger.warning(f"Unknown distance metric '{distance_str}', falling back to COSINE")
            self.distance = Distance.COSINE
        
        # Ensure collection exists
        self._ensure_collection()
    
    def _initialize_client(self) -> QdrantClient:
        """Initialize Qdrant client."""
        try:
            url = self.qdrant_config.get("url", "http://localhost:6333")
            client = QdrantClient(url=url)
            
            # Test connection
            collections = client.get_collections()
            logger.info(f"Successfully connected to Qdrant at {url}")
            return client
        
        except Exception as e:
            logger.error(f"Error connecting to Qdrant: {e}")
            raise
    
    def _ensure_collection(self):
        """Ensure the collection exists, create if it doesn't."""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=self.distance
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add chunks with embeddings to Qdrant."""
        if not chunks:
            return True
        
        try:
            points = []
            for chunk in chunks:
                embedding = chunk.get("embedding")
                if embedding is None:
                    logger.warning(f"No embedding found for chunk {chunk.get('chunk_id', 'unknown')}")
                    continue
                
                # Convert numpy array to list if needed
                if isinstance(embedding, np.ndarray):
                    embedding = embedding.tolist()
                
                # Prepare metadata (exclude embedding to avoid duplication)
                payload = chunk.get("metadata", {}).copy()
                payload["content"] = chunk.get("content", "")
                payload["chunk_id"] = chunk.get("chunk_id")
                
                # Create point
                point = PointStruct(
                    id=chunk.get("chunk_id"),
                    vector=embedding,
                    payload=payload
                )
                points.append(point)
            
            if not points:
                logger.warning("No valid points to add to Qdrant")
                return False
            
            # Upload points
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Successfully added {len(points)} chunks to Qdrant")
            return True
        
        except Exception as e:
            logger.error(f"Error adding chunks to Qdrant: {e}")
            return False
    
    def search_similar(self, query_embedding: Union[np.ndarray, List[float]], 
                      limit: int = 10, score_threshold: float = 0.0,
                      filter_conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar chunks in Qdrant."""
        try:
            # Convert numpy array to list if needed
            if isinstance(query_embedding, np.ndarray):
                query_embedding = query_embedding.tolist()
            
            # Prepare filter if provided
            query_filter = None
            if filter_conditions:
                query_filter = self._build_filter(filter_conditions)
            
            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True,
                with_vectors=False
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    "chunk_id": result.id,
                    "score": result.score,
                    "content": result.payload.get("content", ""),
                    "metadata": {k: v for k, v in result.payload.items() if k != "content"}
                })
            
            logger.info(f"Found {len(results)} similar chunks")
            return results
        
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            return []
    
    def _build_filter(self, conditions: Dict[str, Any]) -> Filter:
        """Build Qdrant filter from conditions."""
        # Simple implementation - can be extended for complex filters
        field_conditions = []
        
        for field, value in conditions.items():
            if isinstance(value, str):
                condition = FieldCondition(
                    key=field,
                    match=MatchValue(value=value)
                )
                field_conditions.append(condition)
        
        return Filter(must=field_conditions) if field_conditions else None
    
    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific chunk by ID."""
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id],
                with_payload=True,
                with_vectors=False
            )
            
            if points:
                point = points[0]
                return {
                    "chunk_id": point.id,
                    "content": point.payload.get("content", ""),
                    "metadata": {k: v for k, v in point.payload.items() if k != "content"}
                }
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving chunk {chunk_id}: {e}")
            return None
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk by ID."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[chunk_id]
            )
            logger.info(f"Deleted chunk {chunk_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting chunk {chunk_id}: {e}")
            return False
    
    def delete_chunks_by_source(self, source_path: str) -> bool:
        """Delete all chunks from a specific source file."""
        try:
            # Create filter for source path
            delete_filter = Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source_path)
                    )
                ]
            )
            
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=delete_filter
            )
            
            logger.info(f"Deleted chunks from source: {source_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting chunks from source {source_path}: {e}")
            return False
        
    def search_similar(self, query_embedding: List[float], limit: int = 10, 
                    score_threshold: float = 0.0, filter_conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for similar vectors in the collection."""
        try:
            # Build filter conditions for Qdrant
            filter_query = None
            if filter_conditions:
                filter_query = models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        ) for key, value in filter_conditions.items()
                    ]
                )
            
            # Perform the search
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=filter_query,
                with_payload=True,
                with_vectors=False
            )
            
            # Convert results to standard format
            results = []
            for point in search_result:
                result = {
                    "chunk_id": str(point.id),
                    "score": point.score,
                    "content": point.payload.get("content", ""),
                    "metadata": {
                        "source": point.payload.get("source", ""),
                        "chunk_index": point.payload.get("chunk_index", 0),
                        "page_number": point.payload.get("page_number"),
                        "type": point.payload.get("type"),
                        "total_chunks": point.payload.get("total_chunks")
                    }
                }
                results.append(result)
            
            logger.debug(f"Found {len(results)} similar vectors")
            return results
        
        except Exception as e:
            logger.error(f"Error searching similar vectors: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "segments_count": info.segments_count,
                "vector_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance.name,
                "status": info.status.name
            }
        
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def health_check(self) -> bool:
        """Check if Qdrant is healthy and accessible."""
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False

# Global Qdrant manager instance
qdrant_manager = QdrantManager()