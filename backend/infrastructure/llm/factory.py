from typing import Dict, Type

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.llm import LLMProvider


class LLMFactory:
    """Factory for creating LLM provider instances."""

    _providers: Dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]) -> None:
        """Register a new LLM provider."""
        cls._providers[name] = provider_class
        logger.info(f"Registered LLM provider: {name}")

    @classmethod
    def create_provider(cls, provider_name: str = None) -> LLMProvider:
        """Create an LLM provider instance."""
        provider_name = provider_name or AppSettings.DEFAULT_LLM_PROVIDER

        if provider_name not in cls._providers:
            raise ValueError(f"Unknown LLM provider: {provider_name}")

        provider_class = cls._providers[provider_name]
        logger.info(f"Creating LLM provider instance: {provider_name}")
        return provider_class()

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get a list of available provider names."""
        return list(cls._providers.keys())
