"""
backend/utils/logger.py
Logging configuration
"""

import logging
import sys
from config.settings import settings


def setup_logger(name: str) -> logging.Logger:
    """Setup configured logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.log_level))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


