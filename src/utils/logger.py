"""Logging utilities for OptimAIze."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Format the log record with colors."""
        # Get the base formatted message
        formatted = super().format(record)
        
        # Add color if outputting to terminal
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            color = self.COLORS.get(record.levelname, '')
            formatted = f"{color}{formatted}{self.RESET}"
        
        return formatted

class OptimAIzeLogger:
    """Custom logger for OptimAIze with enhanced formatting and file rotation."""
    
    def __init__(self):
        """Initialize the logger with configuration."""
        from src.config.settings import config
        
        # Get logging config with fallbacks
        logging_config = getattr(config, 'logging', {})
        log_level = logging_config.get("level", "INFO")
        log_format = logging_config.get("format", "structured")
        file_logging = logging_config.get("file_logging", True)
        log_directory = logging_config.get("log_directory", "data/logs")
        
        self.logger = logging.getLogger("optimaize")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler()
        if log_format == "structured":
            console_formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if file_logging:
            try:
                log_dir = Path(log_directory)
                log_dir.mkdir(parents=True, exist_ok=True)
                
                file_handler = RotatingFileHandler(
                    log_dir / "optimaize.log",
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5
                )
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                # If file logging fails, continue with console only
                print(f"Warning: Could not setup file logging: {e}")
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def debug(self, message, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log info message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log error message."""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(message, *args, **kwargs)

# Global logger instance
logger = OptimAIzeLogger()