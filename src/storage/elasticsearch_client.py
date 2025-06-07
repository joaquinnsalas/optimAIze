"""Elasticsearch client for keyword search in OptimAIze."""

from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from src.config.settings import config
from src.utils.logger import logger

class ElasticsearchManager:
    """Elasticsearch manager for keyword search."""
    
    def __init__(self):
        self.es_config = config.elasticsearch
        self.client = self._initialize_client()
        self.index_name = self.es_config.get("index_name", "optimaize_keywords")
        
        # Ensure index exists
        self._ensure_index()
    
    def _initialize_client(self) -> Elasticsearch:
        """Initialize Elasticsearch client."""
        try:
            url = self.es_config.get("url", "http://localhost:9200")
            client = Elasticsearch([url])
            
            # Test connection
            info = client.info()
            logger.info(f"Successfully connected to Elasticsearch at {url}")
            logger.info(f"Elasticsearch version: {info['version']['number']}")
            return client
        
        except Exception as e:
            logger.error(f"Error connecting to Elasticsearch: {e}")
            raise
    
    def _ensure_index(self):
        """Ensure the index exists, create if it doesn't."""
        try:
            if not self.client.indices.exists(index=self.index_name):
                logger.info(f"Creating index: {self.index_name}")
                
                # Define index mapping
                mapping = {
                    "mappings": {
                        "properties": {
                            "chunk_id": {
                                "type": "keyword"
                            },
                            "content": {
                                "type": "text",
                                "analyzer": "standard",
                                "search_analyzer": "standard"
                            },
                            "source": {
                                "type": "keyword"
                            },
                            "type": {
                                "type": "keyword"
                            },
                            "chunk_index": {
                                "type": "integer"
                            },
                            "chunk_size": {
                                "type": "integer"
                            },
                            "content_preview": {
                                "type": "text"
                            },
                            "file_path": {
                                "type": "keyword"
                            },
                            "processed_time": {
                                "type": "date"
                            }
                        }
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "analysis": {
                            "analyzer": {
                                "custom_text_analyzer": {
                                    "type": "standard",
                                    "stopwords": "_english_"
                                }
                            }
                        }
                    }
                }
                
                self.client.indices.create(
                    index=self.index_name,
                    body=mapping
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
        
        except Exception as e:
            logger.error(f"Error ensuring index exists: {e}")
            raise
    
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add chunks to Elasticsearch for keyword search."""
        if not chunks:
            return True
        
        try:
            # Prepare bulk operations
            bulk_operations = []
            
            for chunk in chunks:
                chunk_id = chunk.get("chunk_id")
                content = chunk.get("content", "")
                metadata = chunk.get("metadata", {})
                
                # Create document for indexing
                doc = {
                    "chunk_id": chunk_id,
                    "content": content,
                    "source": metadata.get("source", ""),
                    "type": metadata.get("type", ""),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "chunk_size": metadata.get("chunk_size", 0),
                    "content_preview": metadata.get("content_preview", ""),
                    "file_path": metadata.get("source", ""),
                    "processed_time": metadata.get("processed_time")
                }
                
                # Add index operation
                bulk_operations.append({
                    "index": {
                        "_index": self.index_name,
                        "_id": chunk_id
                    }
                })
                bulk_operations.append(doc)
            
            if bulk_operations:
                # Perform bulk indexing
                response = self.client.bulk(
                    body=bulk_operations,
                    refresh=True
                )
                
                # Check for errors
                if response.get("errors"):
                    error_count = sum(1 for item in response["items"] if "error" in item.get("index", {}))
                    logger.warning(f"Elasticsearch bulk indexing had {error_count} errors")
                
                logger.info(f"Successfully indexed {len(chunks)} chunks in Elasticsearch")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error adding chunks to Elasticsearch: {e}")
            return False
    
    def search_keywords(self, query: str, limit: int = 10, 
                       filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for chunks using keyword search."""
        try:
            # Build search query
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["content^2", "content_preview"],
                                    "type": "best_fields",
                                    "fuzziness": "AUTO"
                                }
                            }
                        ]
                    }
                },
                "size": limit,
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 150,
                            "number_of_fragments": 3
                        }
                    }
                }
            }
            
            # Add filters if provided
            if filters:
                filter_clauses = []
                for field, value in filters.items():
                    filter_clauses.append({"term": {field: value}})
                
                if filter_clauses:
                    search_body["query"]["bool"]["filter"] = filter_clauses
            
            # Perform search
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Format results
            results = []
            for hit in response["hits"]["hits"]:
                result = {
                    "chunk_id": hit["_id"],
                    "score": hit["_score"],
                    "content": hit["_source"]["content"],
                    "metadata": {
                        k: v for k, v in hit["_source"].items() 
                        if k not in ["content", "chunk_id"]
                    }
                }
                
                # Add highlights if available
                if "highlight" in hit:
                    result["highlights"] = hit["highlight"].get("content", [])
                
                results.append(result)
            
            logger.info(f"Found {len(results)} keyword matches for query: {query}")
            return results
        
        except Exception as e:
            logger.error(f"Error searching Elasticsearch: {e}")
            return []
    
    def search_by_source(self, source_path: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all chunks from a specific source file."""
        try:
            search_body = {
                "query": {
                    "term": {
                        "source": source_path
                    }
                },
                "size": limit,
                "sort": [
                    {"chunk_index": {"order": "asc"}}
                ]
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            results = []
            for hit in response["hits"]["hits"]:
                results.append({
                    "chunk_id": hit["_id"],
                    "content": hit["_source"]["content"],
                    "metadata": {
                        k: v for k, v in hit["_source"].items() 
                        if k not in ["content", "chunk_id"]
                    }
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching by source {source_path}: {e}")
            return []
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk by ID."""
        try:
            self.client.delete(
                index=self.index_name,
                id=chunk_id,
                refresh=True
            )
            logger.info(f"Deleted chunk {chunk_id} from Elasticsearch")
            return True
        
        except NotFoundError:
            logger.warning(f"Chunk {chunk_id} not found in Elasticsearch")
            return False
        except Exception as e:
            logger.error(f"Error deleting chunk {chunk_id}: {e}")
            return False
    
    def delete_chunks_by_source(self, source_path: str) -> bool:
        """Delete all chunks from a specific source file."""
        try:
            delete_query = {
                "query": {
                    "term": {
                        "source": source_path
                    }
                }
            }
            
            response = self.client.delete_by_query(
                index=self.index_name,
                body=delete_query,
                refresh=True
            )
            
            deleted_count = response.get("deleted", 0)
            logger.info(f"Deleted {deleted_count} chunks from source: {source_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting chunks from source {source_path}: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the index."""
        try:
            stats = self.client.indices.stats(index=self.index_name)
            count = self.client.count(index=self.index_name)
            
            index_stats = stats["indices"][self.index_name]
            
            return {
                "index_name": self.index_name,
                "document_count": count["count"],
                "store_size": index_stats["total"]["store"]["size_in_bytes"],
                "segments_count": index_stats["total"]["segments"]["count"],
                "search_queries": index_stats["total"]["search"]["query_total"],
                "indexing_operations": index_stats["total"]["indexing"]["index_total"]
            }
        
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}
    
    def health_check(self) -> bool:
        """Check if Elasticsearch is healthy and accessible."""
        try:
            health = self.client.cluster.health()
            return health["status"] in ["green", "yellow"]
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return False
    
    def refresh_index(self) -> bool:
        """Refresh the index to make recent changes searchable."""
        try:
            self.client.indices.refresh(index=self.index_name)
            return True
        except Exception as e:
            logger.error(f"Error refreshing index: {e}")
            return False

# Global Elasticsearch manager instance
elasticsearch_manager = ElasticsearchManager()