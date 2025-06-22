import time
from typing import List

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchRequest, SearchResponse, SearchResult, StrategyType
from infrastructure.search.factory import SearchStrategyFactory


class SearchService:
    """Service for handling search operations."""

    def __init__(self, strategy_name: StrategyType = StrategyType.DEFAULT, **strategy_kwargs):
        """Initialize the search service.

        Args:
            strategy_name: Name of the search strategy to use
            **strategy_kwargs: Additional arguments for the strategy
        """
        self.strategy = SearchStrategyFactory.create_strategy(strategy_name, **strategy_kwargs)
        logger.info(f"Initialized search service with strategy: {strategy_name}")

    async def search(self, request: SearchRequest) -> SearchResponse:
        """Perform a search operation.

        Args:
            request: The search request

        Returns:
            Search response with results and metadata
        """
        start_time = time.time()

        # Override strategy if specified in request
        if request.search_type != self.strategy.get_strategy_name():
            self.strategy = SearchStrategyFactory.create_strategy(request.search_type, top_k=request.limit)
            logger.info(f"Switched to search strategy: {request.search_type}")

        # Perform search using the strategy
        results = await self.strategy.search(request)

        # Calculate processing time
        server_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        logger.info(f"Search completed in {server_time:.2f}ms for query: {request.query}")

        return SearchResponse(results=results, server_time=server_time, total_results=len(results), query=request.query)

    async def get_available_strategies(self) -> List[str]:
        """Get a list of available search strategies.

        Returns:
            List of strategy names
        """
        return SearchStrategyFactory.get_available_strategies()
