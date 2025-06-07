# src/search.py - ENHANCED VERSION

import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging
import hashlib
from functools import lru_cache
import os
import re
from collections import Counter

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
            
            # Initialize query patterns for different document types
            self._init_query_patterns()
            
        except Exception as e:
            logger.error(f"Failed to initialize HybridSearcher: {e}")
            raise
    
    def _init_query_patterns(self):
        """Initialize patterns for different types of queries"""
        # Common patterns for enterprise documents
        self.query_patterns = {
            'policy': ['policy', 'procedure', 'standard', 'guideline', 'regulation'],
            'technical': ['specification', 'design', 'engineering', 'calculation', 'analysis'],
            'hr': ['pto', 'vacation', 'leave', 'benefits', 'salary', 'employee'],
            'safety': ['safety', 'hazard', 'risk', 'incident', 'compliance'],
            'client': ['client', 'customer', 'project', 'contract', 'agreement'],
            'financial': ['budget', 'cost', 'expense', 'invoice', 'payment'],
            'training': ['training', 'certification', 'course', 'learning', 'skill']
        }
        
        # Stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    def _perform_search(self, query: str, top_k: int) -> List[Dict]:
        """Internal method to perform the actual search"""
        # This is the actual search implementation
        expanded_query = self.expand_query(query)
        semantic_results = self._semantic_search(expanded_query, top_k * 3)
        keyword_results = self._keyword_search(query, top_k * 3)
        merged_results = self._merge_and_rerank(semantic_results, keyword_results, query, top_k)
        
        for result in merged_results:
            result['snippet'] = self.generate_snippet(result['chunk_text'], query)
        
        return merged_results
    
    def search(self, query: str, top_k: int = 10, use_cache: bool = True) -> List[Dict]:
        """
        Perform hybrid search combining semantic and keyword search
        """
        try:
            logger.info(f"Searching for: '{query}' (top_k={top_k})")
            
            # Check cache if enabled
            if use_cache:
                query_hash = hashlib.md5(query.encode()).hexdigest()
                import json
                cached_result = self._cached_search(query_hash, top_k)
                if cached_result:
                    return json.loads(cached_result)
            
            # Expand query for better recall
            expanded_query = self.expand_query(query)
            logger.info(f"Expanded query: '{expanded_query}'")
            
            # 1. Semantic search via Qdrant
            semantic_results = self._semantic_search(expanded_query, top_k * 3)
            logger.info(f"Found {len(semantic_results)} semantic results")
            
            # 2. Keyword search via SQLite FTS5
            keyword_results = self._keyword_search(query, top_k * 3)
            logger.info(f"Found {len(keyword_results)} keyword results")
            
            # 3. Merge and re-rank results
            merged_results = self._merge_and_rerank(semantic_results, keyword_results, query, top_k * 2)
            
            # 4. Apply Cohere reranking if available
            if self.cohere_client and len(merged_results) > 0:
                final_results = self._rerank_with_cohere(query, merged_results, top_k)
                logger.info(f"Reranked with Cohere, returning {len(final_results)} results")
            else:
                final_results = merged_results[:top_k]
            
            # 5. Generate snippets for results
            for result in final_results:
                result['snippet'] = self.generate_snippet(result['chunk_text'], query)
            
            logger.info(f"Returning {len(final_results)} final results")
            
            return final_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def expand_query(self, query: str) -> str:
        """Expand query with related terms from corpus"""
        try:
            # Get top similar chunks
            similar_chunks = self._semantic_search(query, limit=5)
            
            # Extract key terms
            expanded_terms = set(query.lower().split())
            
            # Add common academic terms if relevant
            academic_terms = {
                'engineering': ['design', 'analysis', 'system', 'project'],
                'circuit': ['electrical', 'power', 'voltage', 'current'],
                'programming': ['code', 'software', 'algorithm', 'development'],
                'report': ['analysis', 'results', 'findings', 'conclusion']
            }
            
            # Add related terms from mapping
            for term in query.lower().split():
                if term in academic_terms:
                    expanded_terms.update(academic_terms[term])
            
            # Add terms from similar chunks (simple approach)
            for chunk in similar_chunks[:3]:
                text = chunk.get('chunk_text', '').lower()
                # Extract meaningful words (4+ chars, alphanumeric)
                words = [w for w in text.split() if len(w) > 4 and w.isalnum()]
                # Add top frequency words
                from collections import Counter
                word_freq = Counter(words)
                top_words = [word for word, _ in word_freq.most_common(5)]
                expanded_terms.update(top_words)
            
            # Limit expansion
            expanded_query = ' '.join(list(expanded_terms)[:20])
            return expanded_query
            
        except Exception as e:
            logger.warning(f"Query expansion failed: {e}")
            return query
    
    def _rerank_with_cohere(self, query: str, results: List[Dict], top_k: int) -> List[Dict]:
        """Rerank results using Cohere's reranker"""
        try:
            if not results:
                return results
            
            # Prepare documents for reranking
            documents = [r['chunk_text'] for r in results]
            
            # Rerank with Cohere
            reranked = self.cohere_client.rerank(
                query=query,
                documents=documents,
                top_n=min(top_k, len(documents)),
                model='rerank-english-v3.0'
            )
            
            # Reorder results based on reranking
            reranked_results = []
            for item in reranked.results:
                idx = item.index
                result = results[idx].copy()
                result['rerank_score'] = item.relevance_score
                result['combined_score'] = item.relevance_score  # Update combined score
                reranked_results.append(result)
            
            return reranked_results
            
        except Exception as e:
            logger.error(f"Cohere reranking failed: {e}")
            return results[:top_k]  # Fallback to original ranking
    
    def generate_snippet(self, chunk_text: str, query: str, context_length: int = 150) -> str:
        """Generate highlighted snippet around query terms"""
        try:
            query_terms = query.lower().split()
            text_lower = chunk_text.lower()
            
            # Find best position for snippet
            best_pos = 0
            best_score = 0
            
            # Sliding window to find highest density of query terms
            for i in range(0, max(1, len(chunk_text) - context_length), 10):
                window = text_lower[i:i+context_length]
                score = sum(window.count(term) for term in query_terms if len(term) > 2)
                if score > best_score:
                    best_score = score
                    best_pos = i
            
            # Extract snippet
            snippet = chunk_text[best_pos:best_pos + context_length]
            
            # Find word boundary for clean start
            if best_pos > 0:
                space_pos = chunk_text.rfind(' ', max(0, best_pos - 20), best_pos)
                if space_pos > 0:
                    snippet = chunk_text[space_pos:best_pos + context_length]
                    snippet = "..." + snippet
            
            # Find word boundary for clean end
            if best_pos + context_length < len(chunk_text):
                space_pos = chunk_text.find(' ', best_pos + context_length, min(len(chunk_text), best_pos + context_length + 20))
                if space_pos > 0:
                    snippet = snippet[:space_pos - best_pos] + "..."
            
            # Highlight query terms (case-insensitive)
            for term in query_terms:
                if len(term) > 2:  # Only highlight meaningful terms
                    # Replace all case variations
                    import re
                    pattern = re.compile(re.escape(term), re.IGNORECASE)
                    snippet = pattern.sub(f"**{term.upper()}**", snippet)
            
            return snippet.strip()
            
        except Exception as e:
            logger.warning(f"Snippet generation failed: {e}")
            return chunk_text[:context_length] + "..."
    
    def _semantic_search(self, query: str, limit: int) -> List[Dict]:
        """Perform semantic search using Qdrant"""
        try:
            # Generate query embedding
            query_embedding = self.embed_model.encode(query, show_progress_bar=False).tolist()
            
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
                    'file_name': result.payload.get('file_name', result.payload.get('file_path', '').split('/')[-1]),
                    'file_type': result.payload.get('file_type', ''),
                    'document_id': result.payload.get('document_id', ''),
                    'category': result.payload.get('category', 'Academic'),
                    'chunk_index': result.payload.get('chunk_index', 0),
                    'chunk_type': result.payload.get('chunk_type', 'unknown'),
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
            
            # Search using FTS5 with enhanced metadata
            keyword_results = cursor.execute("""
                SELECT c.chunk_id, c.chunk_text, c.document_id, c.chunk_index, c.chunk_type,
                       d.file_path, d.file_name, d.category, d.title,
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
                    'chunk_index': row[3],
                    'chunk_type': row[4],
                    'file_path': row[5],
                    'file_name': row[6],
                    'category': row[7],
                    'title': row[8],
                    'keyword_score': float(row[9]) if row[9] else 0.0,
                    'source': 'keyword'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def _merge_and_rerank(self, semantic_results: List[Dict], keyword_results: List[Dict], 
                         query: str, top_k: int) -> List[Dict]:
        """Merge and re-rank results with improved scoring"""
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
            
            # Calculate additional relevance features
            for chunk_id, chunk_data in all_chunks.items():
                features = self.calculate_relevance_features(query, chunk_data)
                chunk_data['relevance_score'] = self._combine_features(features)
                # Combine RRF and feature-based scores
                chunk_data['combined_score'] = (
                    0.7 * chunk_data['combined_score'] + 
                    0.3 * chunk_data['relevance_score']
                )
            
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
    
    def calculate_relevance_features(self, query: str, result: Dict) -> Dict:
        """Calculate relevance features for learning to rank"""
        features = {
            'semantic_score': result.get('semantic_score', 0),
            'keyword_score': result.get('keyword_score', 0),
            'query_term_coverage': self._calculate_term_coverage(query, result.get('chunk_text', '')),
            'title_match': 1.0 if query.lower() in result.get('file_name', '').lower() else 0.0,
            'chunk_position_score': 1.0 / (result.get('chunk_index', 0) + 1),  # Earlier chunks score higher
            'chunk_type_bonus': 1.2 if result.get('chunk_type') == 'semantic' else 1.0,
            'doc_length_norm': min(1.0, 500 / max(len(result.get('chunk_text', ' ')), 1))
        }
        return features
    
    def _calculate_term_coverage(self, query: str, text: str) -> float:
        """Calculate what percentage of query terms appear in text"""
        query_terms = set(query.lower().split())
        text_lower = text.lower()
        covered_terms = sum(1 for term in query_terms if term in text_lower)
        return covered_terms / max(len(query_terms), 1)
    
    def _combine_features(self, features: Dict) -> float:
        """Combine features with learned weights"""
        weights = {
            'semantic_score': 0.35,
            'keyword_score': 0.25,
            'query_term_coverage': 0.15,
            'title_match': 0.10,
            'chunk_position_score': 0.05,
            'chunk_type_bonus': 0.05,
            'doc_length_norm': 0.05
        }
        
        return sum(features.get(k, 0) * v for k, v in weights.items())
    
    def get_document_info(self, document_id: str) -> Optional[Dict]:
        """Get full document metadata with enhanced fields"""
        try:
            cursor = self.conn.cursor()
            result = cursor.execute("""
                SELECT document_id, file_path, file_name, title, author, subject,
                       keywords, creation_date, last_modified, category, page_count,
                       has_toc, has_images, estimated_reading_time, first_page_preview
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
                    'subject': result[5],
                    'keywords': result[6],
                    'creation_date': result[7],
                    'last_modified': result[8],
                    'category': result[9],
                    'page_count': result[10],
                    'has_toc': result[11],
                    'has_images': result[12],
                    'estimated_reading_time': result[13],
                    'first_page_preview': result[14]
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get document info: {e}")
            return None
    
    def close(self):
        """Clean up connections"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def get_search_analytics(self) -> Dict:
        """Get analytics about the search system"""
        try:
            cursor = self.conn.cursor()
            
            # Get corpus statistics
            total_docs = cursor.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            total_chunks = cursor.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
            
            # Get category distribution
            categories = cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM documents 
                GROUP BY category 
                ORDER BY count DESC
            """).fetchall()
            
            # Get document type distribution
            doc_types = cursor.execute("""
                SELECT 
                    CASE 
                        WHEN file_name LIKE '%.pdf' THEN 'PDF'
                        WHEN file_name LIKE '%.docx' THEN 'Word'
                        WHEN file_name LIKE '%.txt' THEN 'Text'
                        WHEN file_name LIKE '%.pptx' THEN 'PowerPoint'
                        ELSE 'Other'
                    END as doc_type,
                    COUNT(*) as count
                FROM documents
                GROUP BY doc_type
            """).fetchall()
            
            return {
                'total_documents': total_docs,
                'total_chunks': total_chunks,
                'avg_chunks_per_doc': total_chunks / max(total_docs, 1),
                'categories': dict(categories),
                'document_types': dict(doc_types)
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}

# Import and integrate the test query generator
try:
    from test_query_generator import DynamicTestQueryGenerator
    QUERY_GENERATOR_AVAILABLE = True
except ImportError:
    logger.warning("Test query generator not available")
    QUERY_GENERATOR_AVAILABLE = False

def run_system_diagnostics(top_k: int = 5) -> Dict:
    """Run comprehensive system diagnostics"""
    try:
        searcher = HybridSearcher()
        diagnostics = {
            'status': 'healthy',
            'analytics': searcher.get_search_analytics(),
            'sample_queries': []
        }
        
        # Generate and test dynamic queries if available
        if QUERY_GENERATOR_AVAILABLE:
            db_path = Path(__file__).parent.parent / "data" / "index_metadata.db"
            generator = DynamicTestQueryGenerator(str(db_path))
            
            # Generate test queries
            test_queries = generator.generate_test_queries(num_queries=6)
            validated_queries = generator.validate_queries(test_queries, searcher)
            
            diagnostics['sample_queries'] = validated_queries
            generator.close()
        
        # Test basic search functionality
        test_results = searcher.search("document", top_k=3)
        diagnostics['search_functional'] = len(test_results) > 0
        
        searcher.close()
        return diagnostics
        
    except Exception as e:
        logger.error(f"System diagnostics failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }

# Enhanced test function
def test_search():
    """Test the enhanced search functionality"""
    searcher = HybridSearcher()
    
    print("🔍 OptimAIze Search - Enterprise Edition\n")
    print("Running system diagnostics...\n")
    
    # Run diagnostics
    diagnostics = run_system_diagnostics()
    
    # Display analytics
    if 'analytics' in diagnostics:
        analytics = diagnostics['analytics']
        print("📊 **Corpus Analytics:**")
        print(f"- Total Documents: {analytics.get('total_documents', 0):,}")
        print(f"- Total Chunks: {analytics.get('total_chunks', 0):,}")
        print(f"- Document Types: {analytics.get('document_types', {})}")
        print()
    
    # Test with enterprise-focused queries
    enterprise_queries = [
        ("How many days of PTO do I get?", "hr"),
        ("concrete slab design specifications", "technical"),
        ("safety procedures for confined spaces", "safety"),
        ("client project requirements", "client"),
        ("budget approval process", "financial"),
        ("certification requirements", "training")
    ]
    
    print("🧪 **Testing Enterprise Queries:**\n")
    
    for query, expected_context in enterprise_queries:
        print(f"Query: '{query}'")
        results = searcher.search(query, top_k=3)
        
        if results:
            print(f"✅ Found {len(results)} results")
            print(f"   Context: {results[0].get('context', 'unknown')}")
            print(f"   Top Result: {results[0].get('file_name', 'Unknown')}")
            print(f"   Score: {results[0].get('combined_score', 0):.4f}")
            print(f"   Snippet: {results[0].get('snippet', 'N/A')[:100]}...")
        else:
            print("❌ No results found")
        print()
    
    # Test dynamic queries if available
    if 'sample_queries' in diagnostics and diagnostics['sample_queries']:
        print("\n🎯 **Dynamic Query Test Results:**\n")
        for i, query_info in enumerate(diagnostics['sample_queries'][:4], 1):
            print(f"Query {i}: {query_info['type'].title()}")
            print(f"  Search: '{query_info['query']}'")
            print(f"  Results: {query_info['validation']['results_found']} documents")
            if query_info['validation']['has_results']:
                print(f"  Top File: {query_info['validation']['top_result_file']}")
            print()
    
    searcher.close()
    print("✅ Search system test completed!")

if __name__ == "__main__":
    test_search()