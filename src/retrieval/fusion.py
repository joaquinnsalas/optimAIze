# RRF and weighted fusion algorithms
"""Result fusion algorithms for hybrid search in OptimAIze."""

import math
from typing import List, Dict, Any, Tuple
from src.config.settings import config
from src.utils.logger import logger
from src.retrieval.models import SearchResult

class ResultFusion:
    """Handles fusion of results from multiple search sources."""
    
    def __init__(self):
        self.retrieval_config = config.retrieval
        self.fusion_method = self.retrieval_config.get("fusion_method", "rrf")
        self.rrf_k = self.retrieval_config.get("rrf_k", 60)
        self.semantic_weight = self.retrieval_config.get("semantic_weight", 0.7)
        self.keyword_weight = self.retrieval_config.get("keyword_weight", 0.3)
    
    def fuse_results(self, semantic_results: List[SearchResult], 
                    keyword_results: List[SearchResult],
                    top_k: int = 10) -> Tuple[List[SearchResult], Dict[str, Any]]:
        """Fuse results from semantic and keyword search."""
        try:
            if self.fusion_method == "rrf":
                fused_results, fusion_info = self._reciprocal_rank_fusion(
                    semantic_results, keyword_results, top_k
                )
            elif self.fusion_method == "weighted":
                fused_results, fusion_info = self._weighted_fusion(
                    semantic_results, keyword_results, top_k
                )
            else:
                logger.warning(f"Unknown fusion method '{self.fusion_method}', using RRF")
                fused_results, fusion_info = self._reciprocal_rank_fusion(
                    semantic_results, keyword_results, top_k
                )
            
            logger.info(f"Fused {len(semantic_results)} semantic + {len(keyword_results)} keyword results into {len(fused_results)} final results")
            return fused_results, fusion_info
        
        except Exception as e:
            logger.error(f"Error in result fusion: {e}")
            # Fallback: return semantic results if available, otherwise keyword
            fallback_results = semantic_results[:top_k] if semantic_results else keyword_results[:top_k]
            return fallback_results, {"error": str(e), "method": "fallback"}
    
    def _reciprocal_rank_fusion(self, semantic_results: List[SearchResult],
                               keyword_results: List[SearchResult],
                               top_k: int) -> Tuple[List[SearchResult], Dict[str, Any]]:
        """Implement Reciprocal Rank Fusion (RRF)."""
        
        # Create ranking maps
        semantic_ranks = {result.chunk_id: rank + 1 for rank, result in enumerate(semantic_results)}
        keyword_ranks = {result.chunk_id: rank + 1 for rank, result in enumerate(keyword_results)}
        
        # Combine all unique chunk IDs
        all_chunk_ids = set(semantic_ranks.keys()) | set(keyword_ranks.keys())
        
        # Calculate RRF scores
        rrf_scores = {}
        result_map = {}
        
        # Create result lookup map
        for result in semantic_results + keyword_results:
            if result.chunk_id not in result_map:
                result_map[result.chunk_id] = result
        
        for chunk_id in all_chunk_ids:
            rrf_score = 0.0
            
            # Add semantic contribution
            if chunk_id in semantic_ranks:
                rrf_score += 1.0 / (self.rrf_k + semantic_ranks[chunk_id])
            
            # Add keyword contribution  
            if chunk_id in keyword_ranks:
                rrf_score += 1.0 / (self.rrf_k + keyword_ranks[chunk_id])
            
            rrf_scores[chunk_id] = rrf_score
        
        # Sort by RRF score and create final results
        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        fused_results = []
        for chunk_id, rrf_score in sorted_chunks[:top_k]:
            if chunk_id in result_map:
                result = result_map[chunk_id]
                # Update the result with RRF score and source type
                result.score = rrf_score
                result.source_type = self._determine_source_type(chunk_id, semantic_ranks, keyword_ranks)
                fused_results.append(result)
        
        fusion_info = {
            "method": "rrf",
            "rrf_k": self.rrf_k,
            "semantic_count": len(semantic_results),
            "keyword_count": len(keyword_results),
            "total_unique": len(all_chunk_ids),
            "overlap_count": len(set(semantic_ranks.keys()) & set(keyword_ranks.keys()))
        }
        
        return fused_results, fusion_info
    
    def _weighted_fusion(self, semantic_results: List[SearchResult],
                        keyword_results: List[SearchResult],
                        top_k: int) -> Tuple[List[SearchResult], Dict[str, Any]]:
        """Implement weighted score fusion."""
        
        # Normalize scores to 0-1 range
        semantic_normalized = self._normalize_scores(semantic_results)
        keyword_normalized = self._normalize_scores(keyword_results)
        
        # Create score maps
        semantic_scores = {result.chunk_id: result.score for result in semantic_normalized}
        keyword_scores = {result.chunk_id: result.score for result in keyword_normalized}
        
        # Combine all unique chunk IDs
        all_chunk_ids = set(semantic_scores.keys()) | set(keyword_scores.keys())
        
        # Calculate weighted scores
        weighted_scores = {}
        result_map = {}
        
        # Create result lookup map
        for result in semantic_results + keyword_results:
            if result.chunk_id not in result_map:
                result_map[result.chunk_id] = result
        
        for chunk_id in all_chunk_ids:
            weighted_score = 0.0
            
            # Add semantic contribution
            if chunk_id in semantic_scores:
                weighted_score += self.semantic_weight * semantic_scores[chunk_id]
            
            # Add keyword contribution
            if chunk_id in keyword_scores:
                weighted_score += self.keyword_weight * keyword_scores[chunk_id]
            
            weighted_scores[chunk_id] = weighted_score
        
        # Sort by weighted score and create final results
        sorted_chunks = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
        
        fused_results = []
        for chunk_id, weighted_score in sorted_chunks[:top_k]:
            if chunk_id in result_map:
                result = result_map[chunk_id]
                # Update the result with weighted score and source type
                result.score = weighted_score
                result.source_type = self._determine_source_type(
                    chunk_id, semantic_scores, keyword_scores
                )
                fused_results.append(result)
        
        fusion_info = {
            "method": "weighted",
            "semantic_weight": self.semantic_weight,
            "keyword_weight": self.keyword_weight,
            "semantic_count": len(semantic_results),
            "keyword_count": len(keyword_results),
            "total_unique": len(all_chunk_ids)
        }
        
        return fused_results, fusion_info
    
    def _normalize_scores(self, results: List[SearchResult]) -> List[SearchResult]:
        """Normalize scores to 0-1 range."""
        if not results:
            return results
        
        scores = [result.score for result in results]
        max_score = max(scores) if scores else 1.0
        min_score = min(scores) if scores else 0.0
        
        # Avoid division by zero
        score_range = max_score - min_score
        if score_range == 0:
            for result in results:
                result.score = 1.0
            return results
        
        # Normalize to 0-1 range
        for result in results:
            result.score = (result.score - min_score) / score_range
        
        return results
    
    def _determine_source_type(self, chunk_id: str, 
                              semantic_map: Dict[str, Any], 
                              keyword_map: Dict[str, Any]) -> str:
        """Determine the source type for a result."""
        in_semantic = chunk_id in semantic_map
        in_keyword = chunk_id in keyword_map
        
        if in_semantic and in_keyword:
            return "hybrid"
        elif in_semantic:
            return "semantic"
        elif in_keyword:
            return "keyword"
        else:
            return "unknown"
    
    def get_fusion_stats(self, semantic_results: List[SearchResult],
                        keyword_results: List[SearchResult]) -> Dict[str, Any]:
        """Get statistics about result overlap and distribution."""
        semantic_ids = {result.chunk_id for result in semantic_results}
        keyword_ids = {result.chunk_id for result in keyword_results}
        
        overlap_ids = semantic_ids & keyword_ids
        total_unique = len(semantic_ids | keyword_ids)
        
        return {
            "semantic_only": len(semantic_ids - keyword_ids),
            "keyword_only": len(keyword_ids - semantic_ids),
            "overlap": len(overlap_ids),
            "total_unique": total_unique,
            "overlap_percentage": len(overlap_ids) / total_unique * 100 if total_unique > 0 else 0,
            "semantic_coverage": len(semantic_ids) / total_unique * 100 if total_unique > 0 else 0,
            "keyword_coverage": len(keyword_ids) / total_unique * 100 if total_unique > 0 else 0
        }