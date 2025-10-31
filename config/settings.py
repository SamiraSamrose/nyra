# File: config/settings.py

#"""
#Application settings and configuration management
#Handles environment variables and configuration validation
#"""

import os
from typing import Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Flask configuration
    flask_env: str = os.getenv('FLASK_ENV', 'development')
    secret_key: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    port: int = int(os.getenv('PORT', 5000))
    
    # Google Cloud Platform
    google_cloud_project: str = os.getenv('GOOGLE_CLOUD_PROJECT', '')
    gemini_api_key: str = os.getenv('GEMINI_API_KEY', '')
    firebase_config_path: str = os.getenv('FIREBASE_CONFIG_PATH', 'config/firebase_config.json')
    
    # BigQuery configuration
    bigquery_dataset: str = os.getenv('BIGQUERY_DATASET', 'nyra_analytics')
    bigquery_table: str = os.getenv('BIGQUERY_TABLE', 'user_interactions')
    
    # Application settings
    cors_origins: list = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    max_workers: int = int(os.getenv('MAX_WORKERS', 4))
    rate_limit_per_minute: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # Cache configuration
    enable_cache: bool = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    cache_ttl: int = int(os.getenv('CACHE_TTL', 3600))
    
    # API endpoints
    gemini_nano_endpoint: str = 'chrome-ai://nano'
    gemini_pro_endpoint: str = 'https://generativelanguage.googleapis.com/v1/models/gemini-pro'
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Validate secret key is set in production"""
        if v == 'dev-secret-key' and os.getenv('FLASK_ENV') == 'production':
            raise ValueError('SECRET_KEY must be set in production')
        return v
    
    @validator('gemini_api_key')
    def validate_api_key(cls, v):
        """Validate Gemini API key is configured"""
        if not v:
            raise ValueError('GEMINI_API_KEY must be configured')
        return v
    
    class Config:
        """Pydantic configuration"""
        case_sensitive = False


# Global settings instance
settings = Settings()