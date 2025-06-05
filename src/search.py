# src/search.py

import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths & Config (same as indexer)
# -----------------------------
BASE_DIR = Path(__file__).parent.parent.resolve()
SQLITE_DB = BASE_DIR / "data" / "index_metadata.db"
COLLECTION_NAME = "optimAIze-index"
QDRANT_URL = "http://localhost:6333"

logger = logging.getLogger(__name__)

class HybridSearcher:
    def __init__(self):
        """Initialize the hybrid searcher with all required components"""
        try:
            # Initialize Qdrant
            self.qdrant = QdrantClient(url=QDRANT_URL)
            logger.info("✅ Connected to Qdrant")
            
            # Initialize SQLite
            self.conn = sqlite3.connect(SQLITE_DB)
            logger.info("✅ Connected to SQLite")
            
            # Initialize embedding model
            logger.info("⏳ Loading embedding model...")
            self.embed_model = SentenceTransformer(
                "nomic-ai/nomic-embed-text-v1",
                trust_remote_code=True
            )
            logger.info("✅ Embedding model loaded")
            
        except Exception as e:
            logger.error(f"Failed to initialize HybridSearcher: {e}")
            raise
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Perform hybrid search combining semantic and keyword search
        """
        try:
            logger.info(f"Searching for: '{query}' (top_k={top_k})")
            
            # 1. Semantic search via Qdrant
            semantic_results = self._semantic_search(query, top_k * 2)
            logger.info(f"Found {len(semantic_results)} semantic results")
            
            # 2. Keyword search via SQLite FTS5
            keyword_results = self._keyword_search(query, top_k * 2)
            logger.info(f"Found {len(keyword_results)} keyword results")
            
            # 3. Merge and re-rank results
            final_results = self._merge_and_rerank(semantic_results, keyword_results, query, top_k)
            logger.info(f"Returning {len(final_results)} final results")
            
            return final_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def _semantic_search(self, query: str, limit: int) -> List[Dict]:
        """Perform semantic search using Qdrant"""
        try:
            # Generate query embedding
            query_embedding = self.embed_model.encode(query).tolist()
            
            # Search in Qdrant using the newer query_points method
            search_results = self.qdrant.query_points(
                collection_name=COLLECTION_NAME,
                query=query_embedding,
                limit=limit
            ).points
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    'chunk_id': result.id,
                    'chunk_text': result.payload.get('chunk', ''),
                    'file_path': result.payload.get('file_path', ''),
                    'file_name': result.payload.get('file_path', '').split('/')[-1] if result.payload.get('file_path') else 'Unknown',
                    'file_type': result.payload.get('file_type', ''),
                    'document_id': result.payload.get('document_id', ''),
                    'category': 'Academic',  # Default category
                    'semantic_score': float(result.score),
                    'source': 'semantic'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
    
    def _keyword_search(self, query: str, limit: int) -> List[Dict]:
        """Perform keyword search using SQLite FTS5"""
        try:
            cursor = self.conn.cursor()
            
            # Escape query for FTS5
            fts_query = query.replace('"', '""')
            
            # Search using FTS5
            keyword_results = cursor.execute("""
                SELECT c.chunk_id, c.chunk_text, c.document_id, 
                       d.file_path, 
                       COALESCE(d.file_name, SUBSTR(d.file_path, INSTR(d.file_path, '/') + 1)) as file_name,
                       COALESCE(d.category, 'Academic') as category,
                       bm25(chunks_fts) as score
                FROM chunks_fts
                JOIN chunks c ON chunks_fts.rowid = c.rowid
                JOIN documents d ON c.document_id = d.document_id
                WHERE chunks_fts MATCH ?
                ORDER BY bm25(chunks_fts)
                LIMIT ?
            """, (fts_query, limit)).fetchall()
            
            # Format results
            results = []
            for row in keyword_results:
                results.append({
                    'chunk_id': row[0],
                    'chunk_text': row[1],
                    'document_id': row[2],
                    'file_path': row[3],
                    'file_name': row[4],
                    'category': row[5],
                    'keyword_score': float(row[6]) if row[6] else 0.0,
                    'source': 'keyword'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def _merge_and_rerank(self, semantic_results: List[Dict], keyword_results: List[Dict], 
                         query: str, top_k: int) -> List[Dict]:
        """Merge and re-rank results using Reciprocal Rank Fusion"""
        try:
            # Track all unique chunks
            all_chunks = {}
            
            # Add semantic results with RRF scoring
            for i, result in enumerate(semantic_results):
                chunk_id = result['chunk_id']
                if chunk_id not in all_chunks:
                    all_chunks[chunk_id] = result.copy()
                    all_chunks[chunk_id]['combined_score'] = 0
                
                # Reciprocal Rank Fusion: score = 1 / (rank + k), k=60 is common
                rrf_score = 1 / (i + 60)
                all_chunks[chunk_id]['combined_score'] += rrf_score
                all_chunks[chunk_id]['semantic_rank'] = i + 1
            
            # Add keyword results with RRF scoring
            for i, result in enumerate(keyword_results):
                chunk_id = result['chunk_id']
                if chunk_id not in all_chunks:
                    all_chunks[chunk_id] = result.copy()
                    all_chunks[chunk_id]['combined_score'] = 0
                
                rrf_score = 1 / (i + 60)
                all_chunks[chunk_id]['combined_score'] += rrf_score
                all_chunks[chunk_id]['keyword_rank'] = i + 1
                
                # If this chunk was also found semantically, merge the data
                if 'semantic_score' not in all_chunks[chunk_id]:
                    all_chunks[chunk_id].update(result)
            
            # Sort by combined score and return top_k
            sorted_results = sorted(
                all_chunks.values(), 
                key=lambda x: x['combined_score'], 
                reverse=True
            )
            
            return sorted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Merge and rerank failed: {e}")
            return semantic_results[:top_k] if semantic_results else keyword_results[:top_k]
    
    def get_document_info(self, document_id: str) -> Optional[Dict]:
        """Get full document metadata"""
        try:
            cursor = self.conn.cursor()
            result = cursor.execute("""
                SELECT document_id, file_path, file_name, title, author, 
                       last_modified, category
                FROM documents 
                WHERE document_id = ?
            """, (document_id,)).fetchone()
            
            if result:
                return {
                    'document_id': result[0],
                    'file_path': result[1],
                    'file_name': result[2],
                    'title': result[3],
                    'author': result[4],
                    'last_modified': result[5],
                    'category': result[6]
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get document info: {e}")
            return None
    
    def close(self):
        """Clean up connections"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Test function
def test_search():
    """Test the search functionality"""
    searcher = HybridSearcher()
    
    # Test queries
    test_queries = [
        "engineering project",
        "circuit design",
        "programming",
        "report analysis"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: '{query}'")
        results = searcher.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i} (Score: {result.get('combined_score', 0):.4f})")
            print(f"  File: {result.get('file_name', 'Unknown')}")
            print(f"  Text: {result.get('chunk_text', '')[:100]}...")
    
    searcher.close()

if __name__ == "__main__":
    test_search()