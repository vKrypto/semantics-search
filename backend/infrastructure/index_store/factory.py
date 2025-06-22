from typing import Dict, Type

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.index_store import IndexStoreProvider
from domain.models.index_store import IndexStoreProviderType


class IndexStoreFactory:
    """Factory for creating Index Store Provider instances."""

    _providers: Dict[Type[IndexStoreProviderType], Type[IndexStoreProvider]] = {}

    @classmethod
    def register_provider(cls, name: Type[IndexStoreProviderType], provider_class: Type[IndexStoreProvider]) -> None:
        cls._providers[name] = provider_class
        logger.info(f"Registered Index Store Provider: {name}")

    @classmethod
    def create_provider(cls, provider_name: Type[IndexStoreProviderType] = None, *args, **kwargs) -> IndexStoreProvider:
        provider_name = provider_name or AppSettings.DEFAULT_INDEX_STORE

        if provider_name not in cls._providers:
            raise ValueError(f"Unknown Index Store Provider: {provider_name}")

        provider_class = cls._providers[provider_name]
        logger.info(f"Creating Index Store Provider instance: {provider_name}")
        return provider_class(*args, **kwargs)

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get a list of available provider names."""
        return list(cls._providers.keys())
