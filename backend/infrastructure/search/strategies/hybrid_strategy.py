import time
from operator import itemgetter
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchRequest, SearchResult


class HybridSearchStrategy(SearchStrategy):
    """Hybrid search strategy combining ANN and cosine similarity."""

    def __init__(
        self,
        model: SentenceTransformer,
        index_name: str = "documents",
        top_k: int = 5,
        rerank_k: int = 20,
        min_score: float = 0.30,
        cosine_weight: float = 0.7,
        euclidean_weight: float = 0.3,
    ):
        """Initialize the hybrid search strategy.

        Args:
            model: The sentence transformer model to use
            index_name: Name of the search index
            top_k: Number of results to return
            rerank_k: Number of candidates to rerank
            min_score: Minimum similarity score
            cosine_weight: Weight for cosine similarity
            euclidean_weight: Weight for euclidean distance
        """
        self.model = model
        self.index_name = index_name
        self.top_k = top_k
        self.rerank_k = rerank_k
        self.min_score = min_score
        self.cosine_weight = cosine_weight
        self.euclidean_weight = euclidean_weight
        logger.info(f"Initialized hybrid search with weights: cosine={cosine_weight}, euclidean={euclidean_weight}")

    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        """Normalize a vector."""
        vec = np.array(vec)
        return vec / np.linalg.norm(vec)

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
        """Perform a hybrid search.

        Args:
            request: The search request

        Returns:
            List of search results
        """
        start_time = time.time()

        # Encode query
        query_vector = self._normalize(self.model.encode(request.query.lower()))

        # TODO: Replace with your actual database connector
        # This is where you'd use your Elasticsearch or other vector database
        # For now, returning empty results
        results = []

        # Log search performance
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Hybrid search completed in {search_time:.2f}ms for query: {request.query}")

        return results

    def get_strategy_name(self) -> str:
        """Get the name of the search strategy."""
        return "hybrid"
