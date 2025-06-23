import time
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchRequest, SearchResult


class EuclideanSearchStrategy(SearchStrategy):
    """Search strategy using euclidean distance."""

    def __init__(
        self, model: SentenceTransformer, index_name: str = "documents", top_k: int = 5, max_distance: float = 2.0
    ):
        """Initialize the euclidean search strategy.

        Args:
            model: The sentence transformer model to use
            index_name: Name of the search index
            top_k: Number of results to return
            max_distance: Maximum euclidean distance for results
        """
        self.model = model
        self.index_name = index_name
        self.top_k = top_k
        self.max_distance = max_distance
        logger.info(f"Initialized euclidean search with top_k={top_k}, max_distance={max_distance}")

    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        """Normalize a vector."""
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def _euclidean_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate euclidean distance between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return float(np.linalg.norm(vec1 - vec2))

    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform a euclidean distance search.

        Args:
            request: The search request

        Returns:
            List of search results
        """
        start_time = time.time()

        # Encode query
        query_vector = self._normalize(self.model.encode(request.query.lower()))

        # TODO: Replace with your actual database connector
        # This is where you'd use your vector database to get candidates
        # For each candidate, calculate euclidean distance and filter by max_distance
        # For now, returning empty results
        results = []

        # Log search performance
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Euclidean search completed in {search_time:.2f}ms for query: {request.query}")

        return results

    def get_strategy_name(self) -> str:
        """Get the name of the search strategy."""
        return "euclidean"
