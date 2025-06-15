from typing import Dict, Type

from sentence_transformers import SentenceTransformer

from core.config.settings import AppSettings
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
    def _initialize_model(cls) -> None:
        """Initialize the sentence transformer model if not already initialized."""
        if cls._model is None:
            logger.info(f"Initializing sentence transformer model: {AppSettings.EMBEDDING_MODEL}")
            cls._model = SentenceTransformer(AppSettings.EMBEDDING_MODEL)

    @classmethod
    def create_strategy(cls, strategy_name: str, **kwargs) -> SearchStrategy:
        """Create a search strategy instance.

        Args:
            strategy_name: Name of the strategy to create
            **kwargs: Additional arguments for the strategy

        Returns:
            SearchStrategy instance

        Raises:
            ValueError: If strategy name is not recognized
        """
        if strategy_name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        cls._initialize_model()
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
            name: Name to register the strategy under
            strategy_class: The strategy class to register
        """
        if not issubclass(strategy_class, SearchStrategy):
            raise ValueError("Strategy class must implement SearchStrategy interface")

        cls._strategies[name] = strategy_class
        logger.info(f"Registered new search strategy: {name}")
