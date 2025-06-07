"""File utilities for OptimAIze."""

import hashlib
import os
from pathlib import Path
from typing import List, Tuple, Optional
from src.utils.logger import logger

def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return ""

def get_file_metadata(file_path: Path) -> dict:
    """Get file metadata including size, modification time, and hash."""
    try:
        stat = file_path.stat()
        return {
            "path": str(file_path),
            "size": stat.st_size,
            "modified_time": stat.st_mtime,
            "hash": calculate_file_hash(file_path)
        }
    except Exception as e:
        logger.error(f"Error getting metadata for {file_path}: {e}")
        return {}

def find_files_recursively(root_dir: Path, extensions: List[str]) -> List[Path]:
    """Find all files with specified extensions recursively."""
    if not root_dir.exists():
        logger.warning(f"Root directory does not exist: {root_dir}")
        return []
    
    files = []
    extensions_lower = [ext.lower() for ext in extensions]
    
    try:
        for file_path in root_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions_lower:
                files.append(file_path)
        
        logger.info(f"Found {len(files)} files in {root_dir}")
        return files
    
    except Exception as e:
        logger.error(f"Error finding files in {root_dir}: {e}")
        return []

def is_file_changed(file_path: Path, stored_metadata: Optional[dict]) -> bool:
    """Check if file has changed based on modification time and hash."""
    if not stored_metadata:
        return True
    
    try:
        current_stat = file_path.stat()
        
        # Quick check: modification time
        if current_stat.st_mtime != stored_metadata.get("modified_time"):
            return True
        
        # Thorough check: file hash
        current_hash = calculate_file_hash(file_path)
        return current_hash != stored_metadata.get("hash")
    
    except Exception as e:
        logger.error(f"Error checking if file changed {file_path}: {e}")
        return True

def ensure_directory(directory: Path) -> bool:
    """Ensure directory exists, create if it doesn't."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False

def get_file_size_human_readable(size_bytes: int) -> str:
    """Convert file size to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"