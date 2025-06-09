"""CRUD operations for admin portal."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import AdminSettings, UsageLog, TemplateFile

class AdminCRUD:
    """Admin database operations."""
    
    @staticmethod
    def get_setting(db: Session, key: str, default: Any = None) -> Any:
        """Get admin setting by key."""
        setting = db.query(AdminSettings).filter(AdminSettings.key == key).first()
        if setting:
            try:
                # Try to parse as JSON first
                return json.loads(setting.value)
            except json.JSONDecodeError:
                # Return as string if not JSON
                return setting.value
        return default
    
    @staticmethod
    def set_setting(db: Session, key: str, value: Any, description: str = None) -> AdminSettings:
        """Set admin setting."""
        # Convert value to JSON string
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        
        setting = db.query(AdminSettings).filter(AdminSettings.key == key).first()
        if setting:
            setting.value = value_str
            setting.description = description
            setting.updated_at = datetime.utcnow()
        else:
            setting = AdminSettings(
                key=key,
                value=value_str,
                description=description
            )
            db.add(setting)
        
        db.commit()
        db.refresh(setting)
        return setting
    
    @staticmethod
    def get_all_settings(db: Session) -> Dict[str, Any]:
        """Get all admin settings as dictionary."""
        settings = db.query(AdminSettings).all()
        result = {}
        for setting in settings:
            try:
                result[setting.key] = json.loads(setting.value)
            except json.JSONDecodeError:
                result[setting.key] = setting.value
        return result
    
    @staticmethod
    def log_usage(
        db: Session,
        prompt: str,
        response: str,
        model_name: str,
        tokens_used: int = 0,
        embedding_latency_ms: float = 0.0,
        generation_latency_ms: float = 0.0,
        total_latency_ms: float = 0.0,
        user: str = "admin",
        search_mode: str = "hybrid",
        chunks_retrieved: int = 0
    ) -> UsageLog:
        """Log usage for analytics."""
        log_entry = UsageLog(
            prompt=prompt,
            response=response,
            model_name=model_name,
            tokens_used=tokens_used,
            embedding_latency_ms=embedding_latency_ms,
            generation_latency_ms=generation_latency_ms,
            total_latency_ms=total_latency_ms,
            user=user,
            search_mode=search_mode,
            chunks_retrieved=chunks_retrieved,
            timestamp=datetime.utcnow()
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    
    @staticmethod
    def get_usage_logs(
        db: Session,
        limit: int = 100,
        days_back: int = 90,
        user: Optional[str] = None
    ) -> List[UsageLog]:
        """Get usage logs with filters."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        query = db.query(UsageLog).filter(UsageLog.timestamp >= cutoff_date)
        
        if user:
            query = query.filter(UsageLog.user == user)
        
        return query.order_by(desc(UsageLog.timestamp)).limit(limit).all()
    
    @staticmethod
    def get_usage_stats(db: Session, days_back: int = 30) -> Dict[str, Any]:
        """Get usage statistics."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        logs = db.query(UsageLog).filter(UsageLog.timestamp >= cutoff_date).all()
        
        if not logs:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0,
                "total_tokens": 0,
                "models_used": [],
                "avg_chunks_retrieved": 0
            }
        
        total_queries = len(logs)
        avg_latency = sum(log.total_latency_ms for log in logs) / total_queries
        total_tokens = sum(log.tokens_used for log in logs)
        models_used = list(set(log.model_name for log in logs))
        avg_chunks = sum(log.chunks_retrieved for log in logs) / total_queries if total_queries > 0 else 0
        
        return {
            "total_queries": total_queries,
            "avg_latency_ms": round(avg_latency, 2),
            "total_tokens": total_tokens,
            "models_used": models_used,
            "avg_chunks_retrieved": round(avg_chunks, 2)
        }
    
    @staticmethod
    def cleanup_old_logs(db: Session, days_to_keep: int = 90) -> int:
        """Clean up old usage logs."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        deleted_count = db.query(UsageLog).filter(
            UsageLog.timestamp < cutoff_date
        ).delete()
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def get_template(db: Session, name: str) -> Optional[TemplateFile]:
        """Get template by name."""
        return db.query(TemplateFile).filter(TemplateFile.name == name).first()
    
    @staticmethod
    def get_all_templates(db: Session) -> List[TemplateFile]:
        """Get all templates."""
        return db.query(TemplateFile).all()
    
    @staticmethod
    def save_template(
        db: Session,
        name: str,
        file_path: str,
        content: str,
        description: str = None
    ) -> TemplateFile:
        """Save template to database and file."""
        # Save to file system
        template_path = Path(file_path)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Save to database
        template = db.query(TemplateFile).filter(TemplateFile.name == name).first()
        if template:
            template.content = content
            template.description = description
            template.updated_at = datetime.utcnow()
        else:
            template = TemplateFile(
                name=name,
                file_path=file_path,
                content=content,
                description=description
            )
            db.add(template)
        
        db.commit()
        db.refresh(template)
        return template
    
    @staticmethod
    def init_default_settings(db: Session):
        """Initialize default admin settings."""
        defaults = {
            "active_llm": "ollama",
            "ollama_model": "llama3",
            "retrieval_top_k": 10,
            "query_rewrite_enabled": False,
            "autosuggestion_enabled": True,
            "embedding_model": "nomic-ai/nomic-embed-text-v1",
            "search_mode": "hybrid",
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        for key, value in defaults.items():
            existing = db.query(AdminSettings).filter(AdminSettings.key == key).first()
            if not existing:
                AdminCRUD.set_setting(db, key, value, f"Default {key} setting")
    
    @staticmethod
    def init_default_templates(db: Session):
        """Initialize default templates in database."""
        templates = [
            {
                "name": "default",
                "file_path": "src/llm/templates/default.txt",
                "description": "Default QA template"
            },
            {
                "name": "qa_template", 
                "file_path": "src/llm/templates/qa_template.txt",
                "description": "Q&A focused template"
            }
        ]
        
        for template_info in templates:
            file_path = Path(template_info["file_path"])
            
            # Read existing content if file exists
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # Create default content
                content = """You are a helpful assistant designed to help users navigate a complex set of documents. Answer the user's query based on the following context.

## Context Documents

{context}

## User Question

{query}

## Response

Please provide a helpful answer based solely on the context provided above."""
            
            # Save to database
            existing = db.query(TemplateFile).filter(
                TemplateFile.name == template_info["name"]
            ).first()
            
            if not existing:
                AdminCRUD.save_template(
                    db,
                    template_info["name"],
                    template_info["file_path"],
                    content,
                    template_info["description"]
                )