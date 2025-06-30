"""Main LLM processor for question answering with retrieved context."""

import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from src.utils.logger import logger
from src.retrieval.search_engine import search_engine
from src.llm.ollama_client import ollama_client
from src.llm.models import (
    LLMQuery, LLMResponse, CitationSource, LLMGenerationMetadata,
    OllamaRequest, LLMError
)
from src.retrieval.models import SearchResult

class LLMProcessor:
    """Main processor for LLM-powered question answering."""
    
    def __init__(self):
        # Use simple defaults instead of config dependencies
        self.default_model = "llama3"
        self.default_temperature = 0.7
        self.default_max_tokens = 2048
        self.default_template = "default.txt"
        
        # Template cache
        self._template_cache = {}
        
        # Create templates directory if it doesn't exist
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Create default template if it doesn't exist
        self._ensure_default_template()
        
        logger.info("LLM processor initialized")
    
    def _ensure_default_template(self):
        """Create default template if it doesn't exist."""
        default_template_path = self.templates_dir / "default.txt"
        
        if not default_template_path.exists():
            default_template_content = """You are a helpful assistant designed to help users navigate a complex set of documents. Answer the user's query based on the following context. Follow these rules:

1. Use only information from the provided context.
2. If the context doesn't adequately address the query, say: "Based on the available information, I cannot provide a complete answer to this question."
3. Give clear, concise, and accurate responses. Explain complex terms if needed.
4. If the context contains conflicting information, point this out without attempting to resolve the conflict.
5. Don't use phrases like "according to the context," "as the context states," etc.

Remember, your purpose is to provide information based on the retrieved context, not to offer original advice.

## Context Documents

{context}

## User Question

{query}

## Response

Please provide a helpful answer based solely on the context provided above. If you reference specific information, use numbered citations like [1], [2], etc. that correspond to the document chunks provided."""
            
            with open(default_template_path, 'w', encoding='utf-8') as f:
                f.write(default_template_content)
            
            logger.info(f"Created default template at {default_template_path}")
    
    async def process_query(self, query: LLMQuery) -> LLMResponse:
        """Process a complete query: search + LLM generation."""
        start_time = time.time()
        
        try:
            # Step 1: Perform retrieval search
            logger.info(f"Processing LLM query: '{query.query}'")
            search_start = time.time()
            
            search_response = await search_engine.search(
                query=query.query,
                mode=query.mode,
                top_k=query.top_k,
                min_similarity=query.min_similarity
            )
            
            search_time_ms = (time.time() - search_start) * 1000
            
            # Check if we have search results
            if not search_response.results:
                logger.warning("No search results found for query")
                return self._create_no_results_response(
                    query, search_time_ms, 0, search_response.results
                )
            
            logger.info(f"Found {len(search_response.results)} search results")
            
            # Step 2: Generate LLM response
            generation_start = time.time()
            
            llm_response, llm_error = await self._generate_answer(
                query, search_response.results
            )
            
            generation_time_ms = (time.time() - generation_start) * 1000
            total_time_ms = (time.time() - start_time) * 1000
            
            # Step 3: Handle LLM failure with graceful fallback
            if llm_error:
                logger.warning(f"LLM generation failed: {llm_error.error_message}")
                return self._create_fallback_response(
                    query, search_response.results, search_time_ms, 
                    generation_time_ms, total_time_ms, llm_error
                )
            
            # Step 4: Create successful response
            citations = self._extract_citations(search_response.results)
            
            metadata = {
                "model": query.model or self.default_model,
                "search_time_ms": search_time_ms,
                "generation_time_ms": generation_time_ms,
                "total_time_ms": total_time_ms,
                "search_mode": query.mode,
                "chunks_used": len(search_response.results),
                "chunks_cited": len(citations),
                "ollama_available": True,
                "generation_params": {
                    "temperature": query.temperature or self.default_temperature,
                    "max_tokens": query.max_tokens or self.default_max_tokens
                }
            }
            
            response = LLMResponse(
                query=query.query,
                llm_answer=llm_response.response,
                sources=citations,
                search_results=search_response.results,
                metadata=metadata
            )
            
            logger.info(f"LLM processing completed in {total_time_ms:.1f}ms")
            return response
        
        except Exception as e:
            logger.error(f"LLM processing failed: {e}")
            total_time_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                query=query.query,
                llm_answer="An error occurred while processing your query.",
                sources=[],
                search_results=[],
                metadata={
                    "error": str(e),
                    "total_time_ms": total_time_ms,
                    "ollama_available": False
                }
            )
    
    async def _generate_answer(self, query: LLMQuery, search_results: List[SearchResult]) -> Tuple[Optional[Any], Optional[LLMError]]:
        """Generate answer using Ollama."""
        try:
            # Load prompt template
            template_content = self._load_template(self.default_template)
            
            # Format context from search results
            context = self._format_context(search_results)
            
            # Create complete prompt
            prompt = template_content.format(
                context=context,
                query=query.query
            )
            
            # Prepare Ollama request
            ollama_request = OllamaRequest(
                model=query.model or self.default_model,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": query.temperature or self.default_temperature,
                    "num_predict": query.max_tokens or self.default_max_tokens,
                    "stop": ["## User Question", "## Context", "## Response"]
                }
            )
            
            # Generate response
            async with ollama_client as client:
                return await client.generate(ollama_request)
        
        except Exception as e:
            logger.error(f"Error in LLM generation: {e}")
            return None, LLMError(
                error_type="generation_error",
                error_message=str(e)
            )
    
    def _load_template(self, template_name: str) -> str:
        """Load prompt template from file."""
        if template_name in self._template_cache:
            return self._template_cache[template_name]
        
        # Resolve template path
        if not template_name.endswith('.txt'):
            template_name += '.txt'
        
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            logger.warning(f"Template {template_name} not found, using fallback")
            return self._get_fallback_template()
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            self._template_cache[template_name] = template_content
            logger.debug(f"Loaded template: {template_name}")
            return template_content
        
        except Exception as e:
            logger.error(f"Error loading template {template_name}: {e}")
            return self._get_fallback_template()
    
    def _get_fallback_template(self) -> str:
        """Get basic fallback template if file loading fails."""
        return """You are a helpful assistant. Answer the user's question based on the provided context.

Context:
{context}

Question: {query}

Answer:"""
    
    def _format_context(self, search_results: List[SearchResult]) -> str:
        """Format search results into context for the prompt."""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            # Create context entry
            context_entry = f"[{i}] {result.file_name}"
            
            if result.page_number:
                context_entry += f", Page {result.page_number}"
            
            context_entry += f", Chunk {result.chunk_index + 1}"
            context_entry += f" (Score: {result.score:.3f})"
            context_entry += f"\n{result.content}\n"
            
            context_parts.append(context_entry)
        
        return "\n".join(context_parts)
    
    def _extract_citations(self, search_results: List[SearchResult]) -> List[CitationSource]:
        """Extract citation information from search results."""
        citations = []
        
        for result in search_results:
            citation = CitationSource(
                file_name=result.file_name,
                file_path=result.file_path,
                chunk_index=result.chunk_index,
                page_number=result.page_number,
                content_preview=result.content[:200] + "..." if len(result.content) > 200 else result.content,
                score=result.score,
                source_type=result.source_type
            )
            citations.append(citation)
        
        return citations
    
    def _create_no_results_response(self, query: LLMQuery, search_time_ms: float, 
                                   generation_time_ms: float, search_results: List[SearchResult]) -> LLMResponse:
        """Create response when no search results are found."""
        return LLMResponse(
            query=query.query,
            llm_answer="No relevant information was found to answer this question.",
            sources=[],
            search_results=search_results,
            metadata={
                "search_time_ms": search_time_ms,
                "generation_time_ms": generation_time_ms,
                "total_time_ms": search_time_ms + generation_time_ms,
                "chunks_used": 0,
                "ollama_available": False,
                "fallback_reason": "no_search_results"
            }
        )
    
    def _create_fallback_response(self, query: LLMQuery, search_results: List[SearchResult],
                                 search_time_ms: float, generation_time_ms: float, 
                                 total_time_ms: float, llm_error: LLMError) -> LLMResponse:
        """Create fallback response when LLM generation fails."""
        citations = self._extract_citations(search_results)
        
        # Create a basic answer from search results
        fallback_answer = "LLM is currently unavailable. Here are the most relevant search results:\n\n"
        
        for i, result in enumerate(search_results[:3], 1):
            fallback_answer += f"{i}. {result.file_name} (Score: {result.score:.3f})\n"
            preview = result.content[:300] + "..." if len(result.content) > 300 else result.content
            fallback_answer += f"   {preview}\n\n"
        
        return LLMResponse(
            query=query.query,
            llm_answer=fallback_answer,
            sources=citations,
            search_results=search_results,
            metadata={
                "search_time_ms": search_time_ms,
                "generation_time_ms": generation_time_ms,
                "total_time_ms": total_time_ms,
                "chunks_used": len(search_results),
                "ollama_available": False,
                "fallback_reason": llm_error.error_type,
                "error_message": llm_error.error_message
            }
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of LLM processor components."""
        try:
            # Check Ollama availability
            async with ollama_client as client:
                ollama_healthy, ollama_info = await client.health_check()
            
            return {
                "status": "healthy" if ollama_healthy else "degraded",
                "components": {
                    "ollama": ollama_healthy,
                    "templates": len(self._template_cache)
                },
                "ollama_info": ollama_info,
                "default_model": self.default_model,
                "templates_loaded": list(self._template_cache.keys())
            }
        
        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

# Lazy initialization to avoid import-time issues
_llm_processor = None

def get_llm_processor():
    """Get LLM processor instance with lazy initialization."""
    global _llm_processor
    if _llm_processor is None:
        _llm_processor = LLMProcessor()
    return _llm_processor

# For backward compatibility
llm_processor = get_llm_processor()