"""Data models for retrieval results in OptimAIze."""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

@dataclass
class SearchResult:
    """Standardized search result from hybrid retrieval."""
    
    # Content
    content: str
    chunk_id: str
    
    # File information
    file_path: str
    file_name: str
    
    # Position information
    chunk_index: int
    
    # Scoring (required field)
    score: float
    source_type: str  # "semantic", "keyword", "hybrid"
    
    # Optional fields with defaults
    page_number: Optional[int] = None
    highlights: Optional[List[str]] = None
    file_type: Optional[str] = None
    total_chunks: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        # Clean up None values
        return {k: v for k, v in result.items() if v is not None}
    
    @property
    def file_name_only(self) -> str:
        """Get just the filename without path."""
        return Path(self.file_path).name
    
    def normalize_score(self, max_score: float = 1.0) -> float:
        """Normalize score to 0-1 range."""
        if max_score <= 0:
            return 0.0
        return min(self.score / max_score, 1.0)

@dataclass 
class SearchQuery:
    """Represents a search query with processing parameters."""
    
    raw_query: str
    processed_query: str
    mode: str  # "hybrid", "semantic", "keyword"
    
    # Search parameters
    top_k: int = 10
    min_similarity: float = 0.0
    filters: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate query parameters."""
        if self.mode not in ["hybrid", "semantic", "keyword"]:
            raise ValueError(f"Invalid search mode: {self.mode}")
        
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        
        if not self.processed_query.strip():
            raise ValueError("Query cannot be empty")

@dataclass
class SearchResponse:
    """Complete search response with results and metadata."""
    
    query: str
    mode: str
    results: List[SearchResult]
    
    # Response metadata
    total_found: int
    search_time_ms: float
    sources_searched: List[str]  # ["qdrant", "elasticsearch"]
    
    # Fusion information (for hybrid search)
    fusion_method: Optional[str] = None
    fusion_params: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON API response."""
        return {
            "query": self.query,
            "mode": self.mode,
            "results": [result.to_dict() for result in self.results],
            "metadata": {
                "total_found": self.total_found,
                "search_time_ms": self.search_time_ms,
                "sources_searched": self.sources_searched,
                "fusion_method": self.fusion_method,
                "fusion_params": self.fusion_params
            }
        }
    
    @property
    def has_results(self) -> bool:
        """Check if search returned any results."""
        return len(self.results) > 0
    
    def get_top_sources(self, limit: int = 5) -> List[str]:
        """Get top source files from results."""
        seen_files = set()
        top_files = []
        
        for result in self.results:
            if result.file_name not in seen_files and len(top_files) < limit:
                top_files.append(result.file_name)
                seen_files.add(result.file_name)
        
        return top_files