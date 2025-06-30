"""Text chunking utilities for OptimAIze."""

import uuid
from typing import List, Dict, Any
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config.settings import config
from src.utils.logger import logger

class TextChunker:
    """Text chunking with sentence-aware splitting and token counting."""
    
    def __init__(self):
        self.chunk_size = config.indexing.get("chunk_size", 512)
        self.chunk_overlap = config.indexing.get("chunk_overlap", 50)
        
        # Initialize tokenizer for accurate token counting
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
        except Exception as e:
            logger.warning(f"Could not load tiktoken encoder: {e}. Using character-based approximation.")
            self.tokenizer = None
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size * 4,  # Approximate char to token ratio
            chunk_overlap=self.chunk_overlap * 4,
            length_function=self._token_length,
            separators=[
                "\n\n",  # Paragraph breaks
                "\n",    # Line breaks
                " ",     # Word breaks
                ".",     # Sentence breaks
                "!",     # Exclamation breaks
                "?",     # Question breaks
                ";",     # Semicolon breaks
                ",",     # Comma breaks
                ""       # Character breaks (fallback)
            ]
        )
    
    def _token_length(self, text: str) -> int:
        """Calculate token length of text."""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Fallback: approximate 4 characters per token
            return len(text) // 4
    
    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk a document into smaller pieces with metadata."""
        content = document.get("content", "")
        metadata = document.get("metadata", {})
        
        if not content.strip():
            logger.warning(f"Empty content for document: {metadata.get('source', 'unknown')}")
            return []
        
        try:
            # Split text into chunks
            text_chunks = self.text_splitter.split_text(content)
            
            chunks = []
            for i, chunk_text in enumerate(text_chunks):
                if not chunk_text.strip():
                    continue
                
                chunk_id = str(uuid.uuid4())
                chunk_metadata = {
                    **metadata,  # Inherit document metadata
                    "chunk_index": i,
                    "chunk_id": chunk_id,
                    "chunk_size": self._token_length(chunk_text),
                    "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                    "total_chunks": len(text_chunks)
                }
                
                chunks.append({
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": chunk_metadata
                })
            
            logger.info(f"Created {len(chunks)} chunks for {metadata.get('source', 'unknown')}")
            return chunks
        
        except Exception as e:
            logger.error(f"Error chunking document {metadata.get('source', 'unknown')}: {e}")
            return []
    
    def chunk_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a batch of documents."""
        all_chunks = []
        
        for document in documents:
            chunks = self.chunk_document(document)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} total chunks from {len(documents)} documents")
        return all_chunks
    
    def optimize_chunk_size(self, text: str, target_tokens: int = None) -> List[str]:
        """Optimize chunk size for specific content."""
        if target_tokens is None:
            target_tokens = self.chunk_size
        
        # Temporarily adjust chunk size
        original_size = self.chunk_size
        self.chunk_size = target_tokens
        
        # Update text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=target_tokens * 4,
            chunk_overlap=self.chunk_overlap * 4,
            length_function=self._token_length,
            separators=self.text_splitter._separators
        )
        
        try:
            chunks = self.text_splitter.split_text(text)
            return chunks
        finally:
            # Restore original settings
            self.chunk_size = original_size
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=original_size * 4,
                chunk_overlap=self.chunk_overlap * 4,
                length_function=self._token_length,
                separators=self.text_splitter._separators
            )
    
    def get_chunk_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about chunks."""
        if not chunks:
            return {}
        
        chunk_sizes = [chunk["metadata"]["chunk_size"] for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": sum(chunk_sizes) / len(chunk_sizes),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes),
            "total_tokens": sum(chunk_sizes)
        }