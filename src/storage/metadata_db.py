"""Metadata database management for OptimAIze."""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.config.settings import config
from src.utils.logger import logger

Base = declarative_base()

class FileMetadata(Base):
    """SQLAlchemy model for file metadata."""
    __tablename__ = "file_metadata"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String, unique=True, nullable=False)
    file_hash = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    modified_time = Column(Float, nullable=False)
    processed_time = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
class ChunkMetadata(Base):
    """SQLAlchemy model for chunk metadata."""
    __tablename__ = "chunk_metadata"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_id = Column(String, unique=True, nullable=False)  # UUID for Qdrant
    content_preview = Column(Text, nullable=True)  # First 200 chars
    chunk_size = Column(Integer, nullable=False)
    qdrant_stored = Column(Boolean, default=False)
    elasticsearch_stored = Column(Boolean, default=False)
    created_time = Column(DateTime, default=datetime.utcnow)

class MetadataDB:
    """Database manager for file and chunk metadata."""
    
    def __init__(self):
        self.db_config = config.database
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()
    
    def _create_engine(self):
        """Create database engine based on configuration."""
        if self.db_config.get("type") == "postgresql":
            db_url = self.db_config.get("postgresql_url")
            if not db_url:
                logger.error("PostgreSQL URL not configured, falling back to SQLite")
                return self._create_sqlite_engine()
            return create_engine(db_url)
        else:
            return self._create_sqlite_engine()
    
    def _create_sqlite_engine(self):
        """Create SQLite engine."""
        db_path = Path(self.db_config.get("sqlite_path", "data/metadata.db"))
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return create_engine(f"sqlite:///{db_path}")
    
    def _create_tables(self):
        """Create database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get file metadata by path."""
        with self.get_session() as session:
            try:
                file_meta = session.query(FileMetadata).filter(
                    FileMetadata.file_path == file_path
                ).first()
                
                if file_meta:
                    return {
                        "id": file_meta.id,
                        "file_path": file_meta.file_path,
                        "file_hash": file_meta.file_hash,
                        "file_size": file_meta.file_size,
                        "modified_time": file_meta.modified_time,
                        "processed_time": file_meta.processed_time,
                        "chunk_count": file_meta.chunk_count,
                        "status": file_meta.status,
                        "error_message": file_meta.error_message
                    }
                return None
            except Exception as e:
                logger.error(f"Error getting file metadata for {file_path}: {e}")
                return None
    
    def upsert_file_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Insert or update file metadata."""
        with self.get_session() as session:
            try:
                existing = session.query(FileMetadata).filter(
                    FileMetadata.file_path == metadata["file_path"]
                ).first()
                
                if existing:
                    # Update existing record
                    for key, value in metadata.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                else:
                    # Create new record
                    file_meta = FileMetadata(**metadata)
                    session.add(file_meta)
                
                session.commit()
                return True
            except Exception as e:
                logger.error(f"Error upserting file metadata: {e}")
                session.rollback()
                return False
    
    def add_chunk_metadata(self, chunk_meta: Dict[str, Any]) -> bool:
        """Add chunk metadata."""
        with self.get_session() as session:
            try:
                chunk = ChunkMetadata(**chunk_meta)
                session.add(chunk)
                session.commit()
                return True
            except Exception as e:
                logger.error(f"Error adding chunk metadata: {e}")
                session.rollback()
                return False
    
    def get_chunk_metadata(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all chunk metadata for a file."""
        with self.get_session() as session:
            try:
                chunks = session.query(ChunkMetadata).filter(
                    ChunkMetadata.file_path == file_path
                ).all()
                
                return [{
                    "id": chunk.id,
                    "file_path": chunk.file_path,
                    "chunk_index": chunk.chunk_index,
                    "chunk_id": chunk.chunk_id,
                    "content_preview": chunk.content_preview,
                    "chunk_size": chunk.chunk_size,
                    "qdrant_stored": chunk.qdrant_stored,
                    "elasticsearch_stored": chunk.elasticsearch_stored,
                    "created_time": chunk.created_time
                } for chunk in chunks]
            except Exception as e:
                logger.error(f"Error getting chunk metadata for {file_path}: {e}")
                return []
    
    def update_chunk_storage_status(self, chunk_id: str, qdrant: bool = None, elasticsearch: bool = None) -> bool:
        """Update chunk storage status."""
        with self.get_session() as session:
            try:
                chunk = session.query(ChunkMetadata).filter(
                    ChunkMetadata.chunk_id == chunk_id
                ).first()
                
                if chunk:
                    if qdrant is not None:
                        chunk.qdrant_stored = qdrant
                    if elasticsearch is not None:
                        chunk.elasticsearch_stored = elasticsearch
                    session.commit()
                    return True
                return False
            except Exception as e:
                logger.error(f"Error updating chunk storage status: {e}")
                session.rollback()
                return False
    
    def get_processing_stats(self) -> Dict[str, int]:
        """Get processing statistics."""
        with self.get_session() as session:
            try:
                total_files = session.query(FileMetadata).count()
                completed_files = session.query(FileMetadata).filter(
                    FileMetadata.status == "completed"
                ).count()
                failed_files = session.query(FileMetadata).filter(
                    FileMetadata.status == "failed"
                ).count()
                total_chunks = session.query(ChunkMetadata).count()
                
                return {
                    "total_files": total_files,
                    "completed_files": completed_files,
                    "failed_files": failed_files,
                    "processing_files": total_files - completed_files - failed_files,
                    "total_chunks": total_chunks
                }
            except Exception as e:
                logger.error(f"Error getting processing stats: {e}")
                return {}

# Global metadata database instance
metadata_db = MetadataDB()