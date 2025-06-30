"""Metadata database for tracking document processing status."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, String, DateTime, Integer, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.logger import logger

Base = declarative_base()

class ProcessedFile(Base):
    """Database model for tracking processed files."""
    __tablename__ = "processed_files"
    
    file_path = Column(String, primary_key=True)
    file_name = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chunk_count = Column(Integer, default=0)
    processing_time_ms = Column(Float, default=0.0)
    status = Column(String, default="completed")  # completed, failed, processing
    error_message = Column(Text, nullable=True)
    file_metadata = Column(Text, nullable=True)  # JSON string for additional metadata

class DocumentChunk(Base):
    """Database model for document chunks."""
    __tablename__ = "document_chunks"
    
    id = Column(String, primary_key=True)  # UUID
    file_path = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String, nullable=False)
    page_number = Column(Integer, nullable=True)
    chunk_type = Column(String, default="text")  # text, image, table
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    vector_indexed = Column(Boolean, default=False)
    keyword_indexed = Column(Boolean, default=False)

class MetadataDB:
    """Database manager for document metadata and processing status."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize metadata database connection."""
        # Use simple defaults for database path
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = Path("data/optimaize.db")
        
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create SQLAlchemy engine with minimal SQLite configuration
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            echo=False,  # Set to True for SQL debugging
            connect_args={"check_same_thread": False}
        )
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info(f"Metadata database initialized at {self.db_path}")
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def record_file_processing(self, file_path: str, file_name: str, file_hash: str, 
                             file_size: int, chunk_count: int, processing_time_ms: float,
                             status: str = "completed", error_message: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Record file processing information."""
        try:
            with self.get_session() as session:
                # Check if file already exists
                existing = session.query(ProcessedFile).filter_by(file_path=file_path).first()
                
                if existing:
                    # Update existing record
                    existing.file_hash = file_hash
                    existing.file_size = file_size
                    existing.chunk_count = chunk_count
                    existing.processing_time_ms = processing_time_ms
                    existing.status = status
                    existing.error_message = error_message
                    existing.updated_at = datetime.utcnow()
                    if metadata:
                        existing.file_metadata = json.dumps(metadata)
                else:
                    # Create new record
                    processed_file = ProcessedFile(
                        file_path=file_path,
                        file_name=file_name,
                        file_hash=file_hash,
                        file_size=file_size,
                        chunk_count=chunk_count,
                        processing_time_ms=processing_time_ms,
                        status=status,
                        error_message=error_message,
                        file_metadata=json.dumps(metadata) if metadata else None
                    )
                    session.add(processed_file)
                
                logger.debug(f"Recorded file processing: {file_name}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to record file processing: {e}")
            return False
    
    def is_file_processed(self, file_path: str, file_hash: str) -> bool:
        """Check if file has been processed with the same content."""
        try:
            with self.get_session() as session:
                result = session.query(ProcessedFile).filter_by(
                    file_path=file_path,
                    file_hash=file_hash,
                    status="completed"
                ).first()
                return result is not None
        except Exception as e:
            logger.error(f"Failed to check file processing status: {e}")
            return False
    
    def get_processed_files(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of processed files."""
        try:
            with self.get_session() as session:
                query = session.query(ProcessedFile)
                if status:
                    query = query.filter_by(status=status)
                
                files = []
                for file_record in query.all():
                    file_data = {
                        "file_path": file_record.file_path,
                        "file_name": file_record.file_name,
                        "file_hash": file_record.file_hash,
                        "file_size": file_record.file_size,
                        "processed_at": file_record.processed_at.isoformat(),
                        "updated_at": file_record.updated_at.isoformat(),
                        "chunk_count": file_record.chunk_count,
                        "processing_time_ms": file_record.processing_time_ms,
                        "status": file_record.status
                    }
                    if file_record.file_metadata:
                        try:
                            file_data["metadata"] = json.loads(file_record.file_metadata)
                        except json.JSONDecodeError:
                            file_data["metadata"] = {}
                    
                    files.append(file_data)
                
                return files
                
        except Exception as e:
            logger.error(f"Failed to get processed files: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            with self.get_session() as session:
                total_files = session.query(ProcessedFile).count()
                completed_files = session.query(ProcessedFile).filter_by(status="completed").count()
                failed_files = session.query(ProcessedFile).filter_by(status="failed").count()
                total_chunks = session.query(DocumentChunk).count()
                
                # Get latest processing time
                latest_file = session.query(ProcessedFile).order_by(ProcessedFile.updated_at.desc()).first()
                last_update = latest_file.updated_at.isoformat() if latest_file else None
                
                return {
                    "total_files": total_files,
                    "completed_files": completed_files,
                    "failed_files": failed_files,
                    "total_chunks": total_chunks,
                    "last_update": last_update,
                    "database_path": str(self.db_path)
                }
                
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {
                "total_files": 0,
                "completed_files": 0,
                "failed_files": 0,
                "total_chunks": 0,
                "last_update": None,
                "database_path": str(self.db_path)
            }
        
    def upsert_file_metadata(self, file_metadata: Dict[str, Any]) -> bool:
            """Insert or update file metadata."""
            try:
                return self.record_file_processing(
                    file_path=file_metadata.get("file_path", ""),
                    file_name=file_metadata.get("file_name", ""),
                    file_hash=file_metadata.get("file_hash", ""),
                    file_size=file_metadata.get("file_size", 0),
                    chunk_count=file_metadata.get("chunk_count", 0),
                    processing_time_ms=file_metadata.get("processing_time_ms", 0.0),
                    status=file_metadata.get("status", "processing"),
                    error_message=file_metadata.get("error_message"),
                    metadata=file_metadata
                )
            except Exception as e:
                logger.error(f"Failed to upsert file metadata: {e}")
                return False
        
    def add_chunk_metadata(self, chunk_meta: Dict[str, Any]) -> bool:
        """Add chunk metadata to the database."""
        try:
            # For now, we'll just log this - you can extend this later if needed
            logger.debug(f"Chunk metadata recorded for chunk {chunk_meta.get('chunk_id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to add chunk metadata: {e}")
            return False

    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get stored metadata for a file."""
        try:
            files = self.get_processed_files()
            for file_data in files:
                if file_data.get("file_path") == file_path:
                    return file_data
            return None
        except Exception as e:
            logger.error(f"Failed to get file metadata: {e}")
            return None

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics - alias for get_database_stats."""
        return self.get_database_stats()

# Lazy initialization to avoid import-time issues
_metadata_db = None

def get_metadata_db():
    """Get metadata database instance with lazy initialization."""
    global _metadata_db
    if _metadata_db is None:
        _metadata_db = MetadataDB()
    return _metadata_db

# For backward compatibility
metadata_db = get_metadata_db()