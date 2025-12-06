"""Pydantic configuration validator for environment variables."""

import os
from pydantic import BaseSettings, Field, validator


class AppSettings(BaseSettings):
    """Application settings with validation."""
    
    # Django
    SECRET_KEY: str = Field(
        default="django-insecure-change-me-in-production",
        description="Django secret key"
    )
    DEBUG: bool = Field(default=False, description="Django debug mode")
    ALLOWED_HOSTS: str = Field(
        default="localhost,127.0.0.1",
        description="Comma-separated allowed hosts"
    )
    
    # Database
    DB_ENGINE: str = Field(
        default="django.db.backends.postgresql",
        description="Django database engine"
    )
    DB_NAME: str = Field(default="sysacad", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="postgres", description="Database password")
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    
    # Redis
    REDIS_HOST: str = Field(default="redis", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    
    # Logging
    DJANGO_LOG_LEVEL: str = Field(default="INFO", description="Django log level")
    APP_LOG_LEVEL: str = Field(default="INFO", description="App log level")
    REQUESTS_LOG_LEVEL: str = Field(default="WARNING", description="Requests log level")
    
    # Academic Service
    ACADEMIC_SERVICE_URL: str = Field(
        default="http://academico.universidad.localhost",
        description="Academic service URL"
    )
    ACADEMIC_SERVICE_TIMEOUT: int = Field(
        default=5,
        description="Academic service timeout in seconds"
    )
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("DEBUG", pre=True)
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() == "true"
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def validate_config():
    """Validate configuration at startup."""
    try:
        settings = AppSettings()
        return settings
    except Exception as e:
        raise RuntimeError(f"Configuration validation failed: {str(e)}") from e


# Singleton instance
settings = validate_config()
