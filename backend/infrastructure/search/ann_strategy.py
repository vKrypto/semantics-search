import time
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchRequest, SearchResult


class ANNSearchStrategy(SearchStrategy):
    """Search strategy using Approximate Nearest Neighbors."""

    def __init__(
        self, model: SentenceTransformer, index_name: str = "documents", top_k: int = 5, num_candidates: int = 100
    ):
        """Initialize the ANN search strategy.

        Args:
            model: The sentence transformer model to use
            index_name: Name of the search index
            top_k: Number of results to return
            num_candidates: Number of candidates to consider in ANN search
        """
        self.model = model
        self.index_name = index_name
        self.top_k = top_k
        self.num_candidates = num_candidates
        logger.info(f"Initialized ANN search with top_k={top_k}, num_candidates={num_candidates}")

    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        """Normalize a vector."""
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def _get_ann_query(self, query_vector: np.ndarray) -> dict:
        """Get the ANN query for the vector database.

        Args:
            query_vector: The normalized query vector

        Returns:
            Query dictionary for the vector database
        """
        return {
            "knn": {
                "field": "title_vectors",
                "query_vector": query_vector.tolist(),
                "k": self.num_candidates,
                "num_candidates": self.num_candidates * 2,
            },
            "_source": ["title", "content", "title_vectors"],
        }

    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform an ANN search.

        Args:
            request: The search request

        Returns:
            List of search results
        """
        start_time = time.time()

        # Encode query
        query_vector = self._normalize(self.model.encode(request.query.lower()))

        # Get ANN query
        ann_query = self._get_ann_query(query_vector)

        # TODO: Replace with your actual database connector
        # This is where you'd use your vector database to perform ANN search
        # For now, returning empty results
        results = []

        # Log search performance
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"ANN search completed in {search_time:.2f}ms for query: {request.query}")

        return results

    def get_strategy_name(self) -> str:
        """Get the name of the search strategy."""
        return "ann"
