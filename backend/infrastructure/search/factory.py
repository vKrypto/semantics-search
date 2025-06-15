from typing import Dict, Type

from sentence_transformers import SentenceTransformer

from core.config.settings import get_settings
from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy

from .ann_strategy import ANNSearchStrategy
from .cosine_strategy import CosineSearchStrategy
from .euclidean_strategy import EuclideanSearchStrategy
from .hybrid_strategy import HybridSearchStrategy


class SearchStrategyFactory:
    """Factory for creating search strategy instances."""

    _strategies: Dict[str, Type[SearchStrategy]] = {
        "hybrid": HybridSearchStrategy,
        "cosine": CosineSearchStrategy,
        "euclidean": EuclideanSearchStrategy,
        "ann": ANNSearchStrategy,
    }

    _model: SentenceTransformer = None

    @classmethod
    def initialize(cls, model_name: str = None) -> None:
        """Initialize the factory with a sentence transformer model.

        Args:
            model_name: Name of the sentence transformer model to use
        """
        if cls._model is None:
            settings = get_settings()
            model_name = model_name or settings.EMBEDDING_MODEL
            cls._model = SentenceTransformer(model_name)
            logger.info(f"Initialized search factory with model: {model_name}")

    @classmethod
    def create_strategy(cls, strategy_name: str, **kwargs) -> SearchStrategy:
        """Create a search strategy instance.

        Args:
            strategy_name: Name of the strategy to create
            **kwargs: Additional arguments for the strategy

        Returns:
            Search strategy instance

        Raises:
            ValueError: If strategy_name is not recognized
        """
        if cls._model is None:
            cls.initialize()

        if strategy_name not in cls._strategies:
            raise ValueError(f"Unknown search strategy: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]
        logger.info(f"Creating search strategy: {strategy_name}")

        return strategy_class(model=cls._model, **kwargs)

    @classmethod
    def get_available_strategies(cls) -> list[str]:
        """Get a list of available strategy names.

        Returns:
            List of strategy names
        """
        return list(cls._strategies.keys())

    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type[SearchStrategy]) -> None:
        """Register a new search strategy.

        Args:
            name: Name of the strategy
            strategy_class: The strategy class to register
        """
        cls._strategies[name] = strategy_class
        logger.info(f"Registered search strategy: {name}")
