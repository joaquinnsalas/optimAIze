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
        
        # Auto-detect optimal device if not specified
        config_device = config.embeddings.get("device", "auto")
        self.device = self._get_optimal_device(config_device)
        
        # Initialize the model
        self.model = self._load_model()
        logger.info(f"Embedder initialized with {self.model_name} on {self.device}")
    
    def _get_optimal_device(self, config_device: str) -> str:
        """Automatically detect the best available device."""
        if config_device != "auto":
            # If device is explicitly set in config, validate and use it
            return self._validate_device(config_device)
        
        # Auto-detection logic
        try:
            if torch.cuda.is_available():
                # NVIDIA GPU available (engineering workstations)
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"CUDA GPU detected: {gpu_name}")
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                # Apple Silicon (M1/M2/M3 Mac)
                logger.info("Apple Silicon GPU (MPS) detected")
                return "mps"
            else:
                # Fall back to CPU
                logger.info("No GPU acceleration available, using CPU")
                return "cpu"
        except Exception as e:
            logger.warning(f"Error detecting optimal device: {e}, falling back to CPU")
            return "cpu"
    
    def _validate_device(self, device: str) -> str:
        """Validate that the requested device is available."""
        if device == "cuda":
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"Using CUDA GPU: {gpu_name}")
                return "cuda"
            else:
                logger.warning("CUDA requested but not available, falling back to CPU")
                return "cpu"
        elif device == "mps":
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                logger.info("Using Apple Silicon GPU (MPS)")
                return "mps"
            else:
                logger.warning("MPS requested but not available, falling back to CPU")
                return "cpu"
        elif device == "cpu":
            logger.info("Using CPU as requested")
            return "cpu"
        else:
            logger.warning(f"Unknown device '{device}', falling back to CPU")
            return "cpu"
    
    def _load_model(self) -> SentenceTransformer:
        """Load the sentence transformer model."""
        try:
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
    
    def embed_batch(self, texts: List[str], batch_size: int = None) -> List[np.ndarray]:
        """Embed a batch of texts efficiently."""
        if not texts:
            return []
        
        # Adjust batch size based on device capabilities
        if batch_size is None:
            batch_size = self._get_optimal_batch_size()
        
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
            
            logger.info(f"Successfully embedded {len(non_empty_texts)}/{len(texts)} texts on {self.device}")
            return result
        
        except Exception as e:
            logger.error(f"Error embedding batch of {len(texts)} texts: {e}")
            return [np.zeros(self.dimension, dtype=np.float32) for _ in texts]
    
    def _get_optimal_batch_size(self) -> int:
        """Get optimal batch size based on device type."""
        if self.device == "cuda":
            # Engineering workstations with high-end GPUs can handle larger batches
            return 64
        elif self.device == "mps":
            # Apple Silicon - moderate batch size
            return 32
        else:
            # CPU - smaller batch size
            return 16
    
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
                enriched_chunk["metadata"]["device_used"] = self.device
                enriched_chunks.append(enriched_chunk)
            
            logger.info(f"Added embeddings to {len(enriched_chunks)} chunks using {self.device}")
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
        device_info = {
            "device": self.device,
            "device_name": "CPU"
        }
        
        # Add GPU-specific info
        if self.device == "cuda" and torch.cuda.is_available():
            device_info.update({
                "device_name": torch.cuda.get_device_name(0),
                "cuda_version": torch.version.cuda,
                "gpu_memory": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB"
            })
        elif self.device == "mps":
            device_info["device_name"] = "Apple Silicon GPU"
        
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "max_sequence_length": getattr(self.model, 'max_seq_length', 'unknown'),
            "normalization": True,
            "optimal_batch_size": self._get_optimal_batch_size(),
            **device_info
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