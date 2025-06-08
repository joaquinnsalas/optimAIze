"""SQLAlchemy models for admin portal."""

import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AdminUser(Base):
    """Admin user authentication."""
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class AdminSettings(Base):
    """Admin configuration settings."""
    __tablename__ = "admin_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UsageLog(Base):
    """Usage logging for analytics."""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    tokens_used = Column(Integer, default=0)
    embedding_latency_ms = Column(Float, default=0.0)
    generation_latency_ms = Column(Float, default=0.0)
    total_latency_ms = Column(Float, default=0.0)
    user = Column(String, default="admin")
    timestamp = Column(DateTime, default=datetime.utcnow)
    search_mode = Column(String, default="hybrid")
    chunks_retrieved = Column(Integer, default=0)
    
class TemplateFile(Base):
    """Template management."""
    __tablename__ = "template_files"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database setup
class AdminDatabase:
    """Admin database manager."""
    
    def __init__(self, db_url: str = "sqlite:///./data/admin.db"):
        self.engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        """Get database session."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Global admin database instance
admin_db = AdminDatabase()