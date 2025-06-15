from abc import ABC, abstractmethod
from typing import List

from domain.models.search import SearchRequest, SearchResult


class SearchStrategy(ABC):
    """Abstract base class for search strategies."""

    @abstractmethod
    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform a search using the strategy.

        Args:
            request: The search request containing query and parameters

        Returns:
            List of search results
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of the search strategy.

        Returns:
            The name of the strategy (e.g., 'cosine', 'euclidean', 'hybrid')
        """
        pass
