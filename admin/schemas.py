"""Pydantic schemas for admin portal."""

from datetime import datetime
from typing import Optional, Any, List, Dict
from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str

class AdminUserBase(BaseModel):
    """Base admin user schema."""
    email: EmailStr
    is_active: bool = True

class AdminUserCreate(AdminUserBase):
    """Create admin user schema."""
    password: str

class AdminUser(AdminUserBase):
    """Admin user response schema."""
    id: int
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    """Setting update request."""
    key: str
    value: Any
    description: Optional[str] = None

class SettingResponse(BaseModel):
    """Setting response."""
    key: str
    value: Any
    description: Optional[str]
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TemplateUpdate(BaseModel):
    """Template update request."""
    name: str
    content: str
    description: Optional[str] = None

class TemplateResponse(BaseModel):
    """Template response."""
    id: int
    name: str
    file_path: str
    content: str
    description: Optional[str]
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UsageLogResponse(BaseModel):
    """Usage log response."""
    id: int
    prompt: str
    response: str
    model_name: str
    tokens_used: int
    embedding_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    user: str
    timestamp: datetime
    search_mode: str
    chunks_retrieved: int
    
    class Config:
        from_attributes = True

class UsageStatsResponse(BaseModel):
    """Usage statistics response."""
    total_queries: int
    avg_latency_ms: float
    total_tokens: int
    models_used: List[str]
    avg_chunks_retrieved: float

class DashboardResponse(BaseModel):
    """Dashboard data response."""
    stats: UsageStatsResponse
    recent_logs: List[UsageLogResponse]
    settings: Dict[str, Any]

class LogUsageRequest(BaseModel):
    """Log usage request from main API."""
    prompt: str
    response: str
    model_name: str
    tokens_used: int = 0
    embedding_latency_ms: float = 0.0
    generation_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    user: str = "admin"
    search_mode: str = "hybrid"
    chunks_retrieved: int = 0