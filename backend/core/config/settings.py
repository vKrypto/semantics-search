from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

from domain.models.index_store import IndexStoreProviderType


class AppSettingsClass(BaseSettings):
    """Singleton settings class for the application."""

    ROOT_PATH: str = str(Path(__file__).parent.parent.parent)
    STATIC_DIR: str = str(Path(ROOT_PATH).joinpath("static"))
    # API Settings
    VERSION_STR: str = "/v1"
    APP_PREFIX_STR: str = "/app"
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
    DEFAULT_INDEX_STORE: IndexStoreProviderType = IndexStoreProviderType.ELASTIC_DB
    ELASTIC_URL: str = "http://localhost:9200"
    DEFAULT_INDEX_NAME: str = "documents"
    DEFAULT_INDEX_TYPE: str = "cosine_indexes"

    VECTOR_DB_TYPE: str = "chroma"
    # EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_MODEL: str = "all-mpnet-base-v2"
    MODEL_CACHE_DIR: str = str(Path(ROOT_PATH).joinpath("models_cache"))

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create a single instance that will be used throughout the application
@lru_cache()
def get_settings() -> AppSettingsClass:
    return AppSettingsClass()


AppSettings = get_settings()
