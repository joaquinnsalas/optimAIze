"""Embedding utilities for OptimAIze using nomic-embed-text-v1."""

import numpy as np
from typing import List, Dict, Any, Union
from sentence_transformers import SentenceTransformer
import torch
from src.config.settings import config
from src.utils.logger import logger

class TextEmbedder:
    """Text embedding using nomic-embed-text-v1 model."""
    
    def __init__(self):
        self.model_name = config.embeddings.get("model_name", "nomic-ai/nomic-embed-text-v1")
        self.dimension = config.embeddings.get("dimension", 768)
        self.device = config.embeddings.get("device", "cpu")
        
        # Initialize the model
        self.model = self._load_model()
        logger.info(f"Embedder initialized with {self.model_name} on {self.device}")
    
    def _load_model(self) -> SentenceTransformer:
        """Load the sentence transformer model."""
        try:
            # Check if CUDA is available and requested
            if self.device == "cuda" and not torch.cuda.is_available():
                logger.warning("CUDA requested but not available, falling back to CPU")
                self.device = "cpu"
            
            # Load model with trust_remote_code=True for nomic models
            model = SentenceTransformer(
                self.model_name, 
                device=self.device,
                trust_remote_code=True
            )
            
            # Verify model dimension
            test_embedding = model.encode(["test"])
            actual_dim = test_embedding.shape[1]
            
            if actual_dim != self.dimension:
                logger.warning(f"Model dimension {actual_dim} differs from config {self.dimension}, updating config")
                self.dimension = actual_dim
            
            return model
        
        except Exception as e:
            logger.error(f"Error loading embedding model {self.model_name}: {e}")
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text string."""
        try:
            if not text.strip():
                logger.warning("Empty text provided for embedding")
                return np.zeros(self.dimension)
            
            embedding = self.model.encode([text], normalize_embeddings=True)[0]
            return embedding.astype(np.float32)
        
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            return np.zeros(self.dimension, dtype=np.float32)
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """Embed a batch of texts efficiently."""
        if not texts:
            return []
        
        try:
            # Filter out empty texts but keep track of indices
            non_empty_texts = []
            text_indices = []
            
            for i, text in enumerate(texts):
                if text.strip():
                    non_empty_texts.append(text)
                    text_indices.append(i)
            
            if not non_empty_texts:
                logger.warning("All texts in batch are empty")
                return [np.zeros(self.dimension, dtype=np.float32) for _ in texts]
            
            # Embed non-empty texts in batches
            embeddings = []
            for i in range(0, len(non_empty_texts), batch_size):
                batch = non_empty_texts[i:i + batch_size]
                batch_embeddings = self.model.encode(
                    batch, 
                    normalize_embeddings=True,
                    batch_size=len(batch),
                    show_progress_bar=len(non_empty_texts) > 100
                )
                embeddings.extend(batch_embeddings)
            
            # Create result array with proper indexing
            result = [np.zeros(self.dimension, dtype=np.float32) for _ in texts]
            for embedding, original_idx in zip(embeddings, text_indices):
                result[original_idx] = embedding.astype(np.float32)
            
            logger.info(f"Successfully embedded {len(non_empty_texts)}/{len(texts)} texts")
            return result
        
        except Exception as e:
            logger.error(f"Error embedding batch of {len(texts)} texts: {e}")
            return [np.zeros(self.dimension, dtype=np.float32) for _ in texts]
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed chunks and add embeddings to their metadata."""
        if not chunks:
            return []
        
        try:
            # Extract texts from chunks
            texts = [chunk.get("content", "") for chunk in chunks]
            
            # Get embeddings
            embeddings = self.embed_batch(texts)
            
            # Add embeddings to chunks
            enriched_chunks = []
            for chunk, embedding in zip(chunks, embeddings):
                enriched_chunk = chunk.copy()
                enriched_chunk["embedding"] = embedding
                enriched_chunk["metadata"]["embedding_model"] = self.model_name
                enriched_chunk["metadata"]["embedding_dimension"] = self.dimension
                enriched_chunks.append(enriched_chunk)
            
            logger.info(f"Added embeddings to {len(enriched_chunks)} chunks")
            return enriched_chunks
        
        except Exception as e:
            logger.error(f"Error embedding chunks: {e}")
            return chunks
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        try:
            # Ensure embeddings are normalized
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)
        
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embedding model."""
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "device": self.device,
            "max_sequence_length": getattr(self.model, 'max_seq_length', 'unknown'),
            "normalization": True
        }
    
    def validate_embedding(self, embedding: np.ndarray) -> bool:
        """Validate that an embedding is properly formatted."""
        try:
            if not isinstance(embedding, np.ndarray):
                return False
            
            if embedding.shape != (self.dimension,):
                return False
            
            if not np.isfinite(embedding).all():
                return False
            
            # Check if embedding is normalized (should be close to 1.0)
            norm = np.linalg.norm(embedding)
            if not (0.9 <= norm <= 1.1):
                logger.warning(f"Embedding norm {norm} is not close to 1.0")
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating embedding: {e}")
            return False