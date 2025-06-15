from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class AppSettingsClass(BaseSettings):
    """Singleton settings class for the application."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Semantic Search API"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database Settings
    DATABASE_URL: Optional[str] = None

    # LLM Settings
    OPENAI_APIKEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_LLM_PROVIDER: str = "openai"

    # Search Settings
    VECTOR_DB_TYPE: str = "chroma"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create a single instance that will be used throughout the application
@lru_cache()
def get_settings() -> AppSettingsClass:
    return AppSettingsClass()


AppSettings = get_settings()
