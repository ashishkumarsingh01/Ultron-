"""
Logging configuration for Ultron Agent Kernel.
"""

import logging
import os
from pathlib import Path
from typing import Optional
from pythonjsonlogger import jsonlogger


class UltronLogger:
    """Custom logger for Ultron."""
    
    _loggers = {}
    
    @staticmethod
    def setup_logger(
        name: str,
        level: str = "INFO",
        log_file: Optional[str] = None,
        enable_file_logging: bool = True
    ) -> logging.Logger:
        """Setup and configure a logger.
        
        Args:
            name: Logger name
            level: Logging level
            log_file: Log file path
            enable_file_logging: Enable file logging
            
        Returns:
            Configured logger instance
        """
        if name in UltronLogger._loggers:
            return UltronLogger._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))
        
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        if enable_file_logging and log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level.upper()))
            
            json_format = jsonlogger.JsonFormatter()
            file_handler.setFormatter(json_format)
            logger.addHandler(file_handler)
        
        UltronLogger._loggers[name] = logger
        return logger


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_file_logging: bool = True
) -> logging.Logger:
    """Convenience function to setup logger."""
    return UltronLogger.setup_logger(name, level, log_file, enable_file_logging)