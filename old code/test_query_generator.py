import sqlite3
import logging
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import Counter
import random

logger = logging.getLogger(__name__)

class DynamicTestQueryGenerator:
    def __init__(self, sqlite_db_path: str):
        """Initialize with database connection"""
        self.db_path = sqlite_db_path
        self.conn = sqlite3.connect(sqlite_db_path)
        
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her',
            'its', 'our', 'their', 'page', 'figure', 'table', 'section', 'chapter'
        }
    
    def generate_test_queries(self, num_queries: int = 8) -> List[Dict]:
        """
        Generate test queries based on the actual content in the database
        Returns queries with metadata about expected results
        """
        try:
            # Analyze the corpus to understand content types
            corpus_analysis = self._analyze_corpus()
            
            # Generate different types of queries
            queries = []
            
            # 1. Entity-based queries (companies, people, places)
            entity_queries = self._generate_entity_queries(corpus_analysis)
            queries.extend(entity_queries[:2])
            
            # 2. Topic-based queries (key subjects/themes)
            topic_queries = self._generate_topic_queries(corpus_analysis)
            queries.extend(topic_queries[:2])
            
            # 3. Document type queries
            doc_type_queries = self._generate_document_type_queries(corpus_analysis)
            queries.extend(doc_type_queries[:2])
            
            # 4. Temporal/date-based queries
            temporal_queries = self._generate_temporal_queries(corpus_analysis)
            queries.extend(temporal_queries[:1])
            
            # 5. Cross-document concept queries
            concept_queries = self._generate_concept_queries(corpus_analysis)
            queries.extend(concept_queries[:1])
            
            # Shuffle and return the requested number
            random.shuffle(queries)
            return queries[:num_queries]
            
        except Exception as e:
            logger.error(f"Failed to generate test queries: {e}")
            return self._fallback_queries()
    
    def _analyze_corpus(self) -> Dict:
        """Analyze the corpus to understand content characteristics"""
        try:
            cursor = self.conn.cursor()
            
            # Get document metadata
            docs = cursor.execute("""
                SELECT file_name, category, title, author, file_path, 
                       COUNT(c.chunk_id) as chunk_count
                FROM documents d
                LEFT JOIN chunks c ON d.document_id = c.document_id
                GROUP BY d.document_id
            """).fetchall()
            
            # Get sample chunks for content analysis
            sample_chunks = cursor.execute("""
                SELECT chunk_text 
                FROM chunks 
                ORDER BY RANDOM() 
                LIMIT 100
            """).fetchall()
            
            # Extract key terms from chunks
            all_text = ' '.join([chunk[0] for chunk in sample_chunks])
            key_terms = self._extract_key_terms(all_text)
            
            # Identify document patterns
            file_extensions = {}
            categories = {}
            for doc in docs:
                ext = Path(doc[0]).suffix.lower() if doc[0] else 'unknown'
                file_extensions[ext] = file_extensions.get(ext, 0) + 1
                
                cat = doc[1] or 'uncategorized'
                categories[cat] = categories.get(cat, 0) + 1
            
            # Extract entities (capitalized terms, emails, etc.)
            entities = self._extract_entities(all_text)
            
            return {
                'documents': docs,
                'key_terms': key_terms,
                'file_extensions': file_extensions,
                'categories': categories,
                'entities': entities,
                'total_docs': len(docs),
                'sample_text': all_text[:1000]  # For pattern detection
            }
            
        except Exception as e:
            logger.error(f"Corpus analysis failed: {e}")
            return {}
    
    def _extract_key_terms(self, text: str, min_freq: int = 3) -> List[Tuple[str, int]]:
        """Extract meaningful terms from text"""
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stop words and get frequency
        meaningful_words = [w for w in words if w not in self.stop_words and len(w) > 2]
        word_freq = Counter(meaningful_words)
        
        # Return terms that appear frequently enough
        return [(word, count) for word, count in word_freq.most_common(50) if count >= min_freq]
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract potential entities (names, organizations, etc.)"""
        entities = set()
        
        # Find capitalized words/phrases
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities.update(capitalized)
        
        # Find email domains
        emails = re.findall(r'@(\w+\.(?:com|edu|org|net|gov))', text)
        entities.update(emails)
        
        # Find acronyms
        acronyms = re.findall(r'\b[A-Z]{2,6}\b', text)
        entities.update(acronyms)
        
        # Find course codes or similar patterns
        codes = re.findall(r'\b[A-Z]{3,5}\s*\d{3,4}\b', text)
        entities.update(codes)
        
        return list(entities)[:20]  # Limit to prevent overflow
    
    def _generate_entity_queries(self, analysis: Dict) -> List[Dict]:
        """Generate queries based on detected entities"""
        queries = []
        entities = analysis.get('entities', [])
        
        for entity in entities[:5]:
            queries.append({
                'query': entity,
                'type': 'entity',
                'description': f'Search for references to {entity}',
                'expected_results': 'Should find documents mentioning this entity'
            })
        
        return queries
    
    def _generate_topic_queries(self, analysis: Dict) -> List[Dict]:
        """Generate queries based on key topics/terms"""
        queries = []
        key_terms = analysis.get('key_terms', [])
        
        # Single term queries
        for term, freq in key_terms[:3]:
            queries.append({
                'query': term,
                'type': 'topic',
                'description': f'Search for content about {term}',
                'expected_results': f'Should find {freq} or more relevant chunks'
            })
        
        # Multi-term queries (combine related terms)
        if len(key_terms) >= 4:
            combined_query = f"{key_terms[0][0]} {key_terms[1][0]}"
            queries.append({
                'query': combined_query,
                'type': 'topic_combination',
                'description': f'Search for content combining {key_terms[0][0]} and {key_terms[1][0]}',
                'expected_results': 'Should find documents covering both topics'
            })
        
        return queries
    
    def _generate_document_type_queries(self, analysis: Dict) -> List[Dict]:
        """Generate queries based on document types and categories"""
        queries = []
        categories = analysis.get('categories', {})
        
        for category, count in categories.items():
            if category != 'uncategorized' and count > 1:
                queries.append({
                    'query': category.replace('_', ' '),
                    'type': 'document_type',
                    'description': f'Search for {category} documents',
                    'expected_results': f'Should find {count} documents in this category'
                })
        
        return queries
    
    def _generate_temporal_queries(self, analysis: Dict) -> List[Dict]:
        """Generate queries based on temporal patterns"""
        queries = []
        sample_text = analysis.get('sample_text', '')
        
        # Look for years, dates, or temporal terms
        years = re.findall(r'\b(20\d{2}|19\d{2})\b', sample_text)
        if years:
            year = max(set(years), key=years.count)  # Most common year
            queries.append({
                'query': year,
                'type': 'temporal',
                'description': f'Search for content from {year}',
                'expected_results': f'Should find documents from or mentioning {year}'
            })
        
        # Look for common temporal terms
        temporal_terms = ['schedule', 'deadline', 'date', 'time', 'meeting', 'appointment']
        for term in temporal_terms:
            if term in sample_text.lower():
                queries.append({
                    'query': term,
                    'type': 'temporal',
                    'description': f'Search for time-related content ({term})',
                    'expected_results': f'Should find scheduling or time-related documents'
                })
                break
        
        return queries
    
    def _generate_concept_queries(self, analysis: Dict) -> List[Dict]:
        """Generate queries that should span multiple documents"""
        queries = []
        key_terms = analysis.get('key_terms', [])
        
        if len(key_terms) >= 2:
            # Create a conceptual query using top terms
            concept_query = f"{key_terms[0][0]} analysis"
            queries.append({
                'query': concept_query,
                'type': 'concept',
                'description': f'Search for analytical content about {key_terms[0][0]}',
                'expected_results': 'Should find documents with analysis or discussion'
            })
        
        return queries
    
    def _fallback_queries(self) -> List[Dict]:
        """Fallback queries if analysis fails"""
        return [
            {
                'query': 'document',
                'type': 'fallback',
                'description': 'Basic document search',
                'expected_results': 'Should find any indexed documents'
            },
            {
                'query': 'information',
                'type': 'fallback', 
                'description': 'Basic information search',
                'expected_results': 'Should find informational content'
            }
        ]
    
    def validate_queries(self, queries: List[Dict], searcher) -> List[Dict]:
        """Test queries against the search system and validate results"""
        validated_queries = []
        
        for query_info in queries:
            try:
                # Test the query
                results = searcher.search(query_info['query'], top_k=3)
                
                # Add validation info
                query_info['validation'] = {
                    'results_found': len(results),
                    'avg_score': sum(r.get('combined_score', 0) for r in results) / max(len(results), 1),
                    'has_results': len(results) > 0,
                    'top_result_file': results[0].get('file_name', 'None') if results else 'None'
                }
                
                validated_queries.append(query_info)
                
            except Exception as e:
                logger.warning(f"Query validation failed for '{query_info['query']}': {e}")
                continue
        
        return validated_queries
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Test function
def test_dynamic_queries():
    """Test the dynamic query generator"""
    from search import HybridSearcher
    
    # Initialize components
    db_path = Path(__file__).parent.parent / "data" / "index_metadata.db"
    generator = DynamicTestQueryGenerator(str(db_path))
    searcher = HybridSearcher()
    
    print("🔍 Analyzing your corpus and generating test queries...\n")
    
    # Generate queries
    queries = generator.generate_test_queries(num_queries=6)
    
    # Validate queries
    validated_queries = generator.validate_queries(queries, searcher)
    
    print("📊 **Generated Test Queries Based on Your Content:**\n")
    
    for i, query_info in enumerate(validated_queries, 1):
        print(f"**Query {i}: {query_info['type'].title()}**")
        print(f"  Search: '{query_info['query']}'")
        print(f"  Purpose: {query_info['description']}")
        print(f"  Results: {query_info['validation']['results_found']} documents found")
        if query_info['validation']['has_results']:
            print(f"  Top Result: {query_info['validation']['top_result_file']}")
            print(f"  Avg Score: {query_info['validation']['avg_score']:.4f}")
        print()
    
    # Clean up
    generator.close()
    searcher.close()

if __name__ == "__main__":
    test_dynamic_queries()