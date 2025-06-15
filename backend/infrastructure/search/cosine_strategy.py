import time
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchRequest, SearchResult


class CosineSearchStrategy(SearchStrategy):
    """Search strategy using cosine similarity."""

    def __init__(
        self, model: SentenceTransformer, index_name: str = "documents", top_k: int = 5, min_score: float = 0.30
    ):
        """Initialize the cosine search strategy.

        Args:
            model: The sentence transformer model to use
            index_name: Name of the search index
            top_k: Number of results to return
            min_score: Minimum similarity score
        """
        self.model = model
        self.index_name = index_name
        self.top_k = top_k
        self.min_score = min_score
        logger.info(f"Initialized cosine search with top_k={top_k}, min_score={min_score}")

    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        """Normalize a vector."""
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return -1
        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform a cosine similarity search.

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
        # For each candidate, calculate cosine similarity and filter by min_score
        # For now, returning empty results
        results = []

        # Log search performance
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Cosine search completed in {search_time:.2f}ms for query: {request.query}")

        return results

    def get_strategy_name(self) -> str:
        """Get the name of the search strategy."""
        return "cosine"
