"""
Application Configuration

This module contains the application settings and configuration.
Settings are loaded from environment variables with sensible defaults.
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    PROJECT_NAME: str = "AI Meeting Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./meeting_assistant.db"
    DATABASE_ECHO: bool = False  # Set to True to log SQL queries

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # LLM Configuration (to be configured in future episodes)
    LLM_PROVIDER: str = "anthropic"  # Options: anthropic, openai, etc.
    LLM_MODEL: str = "claude-sonnet-4-20250514"
    LLM_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

