"""
Application Configuration

This module contains the application settings and configuration.
Settings are loaded from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "AI Meeting Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./meetings.db"
    
    # LLM Configuration (to be configured in future episodes)
    LLM_PROVIDER: str = "anthropic"  # Options: anthropic, openai, etc.
    LLM_MODEL: str = "claude-sonnet-4-20250514"
    LLM_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

