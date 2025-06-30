# Query preprocessing & validation
"""Query preprocessing for OptimAIze retrieval."""

import re
from typing import Dict, Any
from src.config.settings import config
from src.utils.logger import logger
from src.retrieval.models import SearchQuery

class QueryProcessor:
    """Handles query preprocessing and validation."""
    
    def __init__(self):
        self.retrieval_config = config.retrieval
        self.preprocessing_enabled = self.retrieval_config.get("query_preprocessing", True)
        self.max_query_length = self.retrieval_config.get("max_query_length", 1000)
    
    def process_query(self, raw_query: str, mode: str = "hybrid", 
                     top_k: int = None, min_similarity: float = None,
                     filters: Dict[str, Any] = None) -> SearchQuery:
        """Process and validate a search query."""
        try:
            # Basic validation
            if not raw_query or not raw_query.strip():
                raise ValueError("Query cannot be empty")
            
            # Apply length limit
            if len(raw_query) > self.max_query_length:
                logger.warning(f"Query truncated from {len(raw_query)} to {self.max_query_length} characters")
                raw_query = raw_query[:self.max_query_length]
            
            # Process the query
            processed_query = self._preprocess_text(raw_query) if self.preprocessing_enabled else raw_query.strip()
            
            # Set defaults from config
            if top_k is None:
                top_k = self.retrieval_config.get("final_top_k", 10)
            
            if min_similarity is None:
                min_similarity = self.retrieval_config.get("min_similarity_threshold", 0.0)
            
            return SearchQuery(
                raw_query=raw_query,
                processed_query=processed_query,
                mode=mode,
                top_k=top_k,
                min_similarity=min_similarity,
                filters=filters
            )
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """Apply basic text preprocessing."""
        try:
            # Strip whitespace
            text = text.strip()
            
            # Convert to lowercase for keyword search consistency
            text = text.lower()
            
            # Remove excessive whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove special characters that might interfere with search
            # Keep alphanumeric, spaces, and basic punctuation
            text = re.sub(r'[^\w\s\-\.\,\?\!\:\;\'\"]+', ' ', text)
            
            # Final cleanup
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        
        except Exception as e:
            logger.error(f"Error in text preprocessing: {e}")
            return text.strip()  # Fallback to basic strip
    
    def validate_search_mode(self, mode: str) -> str:
        """Validate and normalize search mode."""
        valid_modes = ["hybrid", "semantic", "keyword"]
        mode = mode.lower().strip()
        
        if mode not in valid_modes:
            logger.warning(f"Invalid search mode '{mode}', defaulting to 'hybrid'")
            return "hybrid"
        
        return mode
    
    def extract_filters_from_query(self, query: str) -> tuple[str, Dict[str, Any]]:
        """Extract filters from query text (e.g., 'safety filetype:pdf')."""
        filters = {}
        cleaned_query = query
        
        # Extract filetype filter
        filetype_match = re.search(r'filetype:(\w+)', query, re.IGNORECASE)
        if filetype_match:
            filters['type'] = filetype_match.group(1).lower()
            cleaned_query = re.sub(r'filetype:\w+', '', cleaned_query, flags=re.IGNORECASE)
        
        # Extract source filter
        source_match = re.search(r'source:([^\s]+)', query, re.IGNORECASE)
        if source_match:
            filters['source'] = source_match.group(1)
            cleaned_query = re.sub(r'source:[^\s]+', '', cleaned_query, flags=re.IGNORECASE)
        
        # Clean up the query
        cleaned_query = re.sub(r'\s+', ' ', cleaned_query).strip()
        
        return cleaned_query, filters if filters else None
    
    def suggest_query_improvements(self, query: str) -> Dict[str, Any]:
        """Suggest improvements for poorly performing queries."""
        suggestions = []
        
        # Too short
        if len(query.strip().split()) < 2:
            suggestions.append("Try using more specific keywords")
        
        # Too long
        if len(query.strip().split()) > 20:
            suggestions.append("Try breaking down into more specific questions")
        
        # All caps
        if query.isupper() and len(query) > 10:
            suggestions.append("Avoid using all capital letters")
        
        # Too many special characters
        special_char_ratio = len(re.findall(r'[^\w\s]', query)) / len(query) if query else 0
        if special_char_ratio > 0.3:
            suggestions.append("Try using fewer special characters")
        
        return {
            "has_suggestions": len(suggestions) > 0,
            "suggestions": suggestions,
            "original_query": query,
            "word_count": len(query.strip().split())
        }
    
    def get_query_stats(self, query: str) -> Dict[str, Any]:
        """Get statistics about a query."""
        words = query.strip().split()
        
        return {
            "character_count": len(query),
            "word_count": len(words),
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "has_numbers": bool(re.search(r'\d', query)),
            "has_special_chars": bool(re.search(r'[^\w\s]', query)),
            "is_question": query.strip().endswith('?'),
            "estimated_complexity": self._estimate_query_complexity(query)
        }
    
    def _estimate_query_complexity(self, query: str) -> str:
        """Estimate query complexity for optimization hints."""
        words = query.strip().split()
        word_count = len(words)
        
        if word_count <= 2:
            return "simple"
        elif word_count <= 8:
            return "moderate"
        else:
            return "complex"