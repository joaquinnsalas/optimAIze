"""Main indexing pipeline for OptimAIze."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from tqdm import tqdm

from src.config.settings import config
from src.utils.logger import logger
from src.utils.file_utils import (
    find_files_recursively, 
    get_file_metadata, 
    is_file_changed
)
from src.storage.metadata_db import metadata_db
from src.storage.qdrant_client import qdrant_manager
from src.storage.elasticsearch_client import elasticsearch_manager
from src.indexing.file_loader import FileLoader
from src.indexing.chunker import TextChunker
from src.indexing.embedder import TextEmbedder

class IndexingPipeline:
    """Main indexing pipeline that coordinates file processing."""
    
    def __init__(self):
        self.config = config.indexing
        self.input_directory = Path(self.config.get("input_directory", "data/documents"))
        self.supported_extensions = self.config.get("supported_extensions", [])
        self.batch_size = self.config.get("batch_size", 100)
        
        # Initialize components
        self.file_loader = FileLoader()
        self.chunker = TextChunker()
        self.embedder = TextEmbedder()
        
        logger.info("Indexing pipeline initialized")
    
    def run_full_pipeline(self, force_reprocess: bool = False) -> Dict[str, Any]:
        """Run the complete indexing pipeline."""
        logger.info("Starting full indexing pipeline")
        start_time = datetime.now()
        
        # Find all files
        files = find_files_recursively(self.input_directory, self.supported_extensions)
        if not files:
            logger.warning(f"No files found in {self.input_directory}")
            return {"status": "completed", "files_processed": 0, "chunks_created": 0}
        
        # Filter files that need processing
        files_to_process = self._filter_files_for_processing(files, force_reprocess)
        
        if not files_to_process:
            logger.info("No files need processing")
            return {"status": "completed", "files_processed": 0, "chunks_created": 0}
        
        logger.info(f"Processing {len(files_to_process)} files")
        
        # Process files in batches
        total_chunks = 0
        processed_files = 0
        failed_files = []
        
        for i in range(0, len(files_to_process), self.batch_size):
            batch = files_to_process[i:i + self.batch_size]
            batch_result = self._process_file_batch(batch)
            
            total_chunks += batch_result["chunks_created"]
            processed_files += batch_result["files_processed"]
            failed_files.extend(batch_result["failed_files"])
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        result = {
            "status": "completed",
            "files_processed": processed_files,
            "chunks_created": total_chunks,
            "failed_files": failed_files,
            "duration_seconds": duration,
            "processing_rate": processed_files / duration if duration > 0 else 0
        }
        
        logger.info(f"Pipeline completed: {result}")
        return result
    
    def _filter_files_for_processing(self, files: List[Path], force_reprocess: bool) -> List[Path]:
        """Filter files that need processing."""
        if force_reprocess:
            return files
        
        files_to_process = []
        
        for file_path in files:
            try:
                # Get current file metadata
                current_metadata = get_file_metadata(file_path)
                if not current_metadata:
                    continue
                
                # Check if file has been processed before
                stored_metadata = metadata_db.get_file_metadata(str(file_path))
                
                if is_file_changed(file_path, stored_metadata):
                    files_to_process.append(file_path)
                else:
                    logger.debug(f"Skipping unchanged file: {file_path}")
            
            except Exception as e:
                logger.error(f"Error checking file {file_path}: {e}")
                files_to_process.append(file_path)  # Process if unsure
        
        return files_to_process
    
    def _process_file_batch(self, files: List[Path]) -> Dict[str, Any]:
        """Process a batch of files."""
        logger.info(f"Processing batch of {len(files)} files")
        
        chunks_created = 0
        files_processed = 0
        failed_files = []
        
        with tqdm(files, desc="Processing files") as pbar:
            for file_path in pbar:
                try:
                    pbar.set_description(f"Processing {file_path.name}")
                    
                    # Update file status to processing
                    file_metadata = get_file_metadata(file_path)
                    if file_metadata:
                        file_metadata["file_path"] = file_metadata.pop("path", str(file_path))  # Fix key name
                        file_metadata["status"] = "processing"
                        file_metadata["processed_time"] = datetime.utcnow()
                        metadata_db.upsert_file_metadata(file_metadata)
                    
                    # Process single file
                    result = self._process_single_file(file_path)
                    
                    if result["success"]:
                        chunks_created += result["chunks_created"]
                        files_processed += 1
                        
                        # Update file status to completed
                        if file_metadata:
                            file_metadata["file_path"] = file_metadata.get("file_path", str(file_path))
                            file_metadata["status"] = "completed"
                            file_metadata["chunk_count"] = result["chunks_created"]
                            metadata_db.upsert_file_metadata(file_metadata)
                    else:
                        failed_files.append({
                            "file": str(file_path),
                            "error": result.get("error", "Unknown error")
                        })
                        
                        # Update file status to failed
                        if file_metadata:
                            file_metadata["file_path"] = file_metadata.get("file_path", str(file_path))
                            file_metadata["status"] = "failed"
                            file_metadata["error_message"] = result.get("error", "Unknown error")
                            metadata_db.upsert_file_metadata(file_metadata)
                
                except Exception as e:
                    error_msg = f"Unexpected error processing {file_path}: {e}"
                    logger.error(error_msg)
                    failed_files.append({
                        "file": str(file_path),
                        "error": error_msg
                    })
        
        return {
            "files_processed": files_processed,
            "chunks_created": chunks_created,
            "failed_files": failed_files
        }
    
    def _process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file through the complete pipeline."""
        try:
            logger.debug(f"Processing file: {file_path}")
            
            # 1. Load file content
            document = self.file_loader.load_file(file_path)
            if not document or not document.get("content"):
                return {"success": False, "error": "Failed to load file content"}
            
            # 2. Chunk the document
            chunks = self.chunker.chunk_document(document)
            if not chunks:
                return {"success": False, "error": "No chunks created from document"}
            
            # 3. Generate embeddings
            enriched_chunks = self.embedder.embed_chunks(chunks)
            if not enriched_chunks:
                return {"success": False, "error": "Failed to generate embeddings"}
            
            # 4. Store in vector database (Qdrant)
            qdrant_success = qdrant_manager.add_chunks(enriched_chunks)
            if not qdrant_success:
                logger.warning(f"Failed to store chunks in Qdrant for {file_path}")
            
            # 5. Store in keyword search (Elasticsearch)
            es_success = elasticsearch_manager.add_chunks(enriched_chunks)
            if not es_success:
                logger.warning(f"Failed to store chunks in Elasticsearch for {file_path}")
            
            # 6. Store chunk metadata in database
            for chunk in enriched_chunks:
                chunk_meta = {
                    "file_path": str(file_path),
                    "chunk_index": chunk["metadata"]["chunk_index"],
                    "chunk_id": chunk["chunk_id"],
                    "content_preview": chunk["metadata"]["content_preview"],
                    "chunk_size": chunk["metadata"]["chunk_size"],
                    "qdrant_stored": qdrant_success,
                    "elasticsearch_stored": es_success,
                    "created_time": datetime.utcnow()
                }
                metadata_db.add_chunk_metadata(chunk_meta)
            
            logger.info(f"Successfully processed {file_path}: {len(enriched_chunks)} chunks created")
            
            return {
                "success": True,
                "chunks_created": len(enriched_chunks),
                "qdrant_stored": qdrant_success,
                "elasticsearch_stored": es_success
            }
        
        except Exception as e:
            error_msg = f"Error processing file {file_path}: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def reprocess_file(self, file_path: Path) -> Dict[str, Any]:
        """Reprocess a specific file, removing old chunks first."""
        try:
            logger.info(f"Reprocessing file: {file_path}")
            
            # Remove existing chunks
            self._remove_file_chunks(file_path)
            
            # Process the file
            return self._process_single_file(file_path)
        
        except Exception as e:
            error_msg = f"Error reprocessing file {file_path}: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def _remove_file_chunks(self, file_path: Path):
        """Remove all chunks for a specific file from all storage systems."""
        try:
            source_path = str(file_path)
            
            # Remove from Qdrant
            qdrant_manager.delete_chunks_by_source(source_path)
            
            # Remove from Elasticsearch
            elasticsearch_manager.delete_chunks_by_source(source_path)
            
            # Note: Chunk metadata in SQLite will be overwritten when new chunks are added
            
            logger.info(f"Removed existing chunks for {file_path}")
        
        except Exception as e:
            logger.error(f"Error removing chunks for {file_path}: {e}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status and statistics."""
        try:
            # Get database stats
            db_stats = metadata_db.get_processing_stats()
            
            # Get storage stats
            qdrant_info = qdrant_manager.get_collection_info()
            es_info = elasticsearch_manager.get_index_stats()
            
            # Health checks
            qdrant_healthy = qdrant_manager.health_check()
            es_healthy = elasticsearch_manager.health_check()
            
            return {
                "database_stats": db_stats,
                "qdrant_info": qdrant_info,
                "elasticsearch_info": es_info,
                "health_status": {
                    "qdrant": qdrant_healthy,
                    "elasticsearch": es_healthy,
                    "overall": qdrant_healthy and es_healthy
                },
                "embedder_info": self.embedder.get_model_info()
            }
        
        except Exception as e:
            logger.error(f"Error getting pipeline status: {e}")
            return {"error": str(e)}

# Global pipeline instance
indexing_pipeline = IndexingPipeline()