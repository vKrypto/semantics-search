"""
Need Full Semantic Search
"""

from domain.models.search import StrategyType

from .factory import SearchStrategyFactory
from .strategies import ANNSearchStrategy, CosineSearchStrategy, EuclideanSearchStrategy, HybridSearchStrategy

SearchStrategyFactory.register_strategy(StrategyType.DEFAULT, CosineSearchStrategy)
SearchStrategyFactory.register_strategy(StrategyType.COSINE, CosineSearchStrategy)
SearchStrategyFactory.register_strategy(StrategyType.HYBRID, HybridSearchStrategy)
SearchStrategyFactory.register_strategy(StrategyType.EUCLIDIAN, EuclideanSearchStrategy)
SearchStrategyFactory.register_strategy(StrategyType.ANN, ANNSearchStrategy)


__all__ = [
    "SearchStrategyFactory",
    "HybridSearchStrategy",
    "EuclideanSearchStrategy",
    "CosineSearchStrategy",
    "ANNSearchStrategy",
]
