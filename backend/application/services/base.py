from typing import Generic, Optional, TypeVar

from core.logging.logger import logger
from domain.interfaces.repository import Repository

T = TypeVar("T")


class BaseService(Generic[T]):
    """Base service class with common functionality."""

    def __init__(self, repository: Repository[T]):
        self.repository = repository
        self.logger = logger

    async def create(self, entity: T) -> T:
        """Create a new entity."""
        self.logger.info(f"Creating new entity: {type(entity).__name__}")
        return await self.repository.create(entity)

    async def get(self, id: str) -> Optional[T]:
        """Get an entity by ID."""
        self.logger.info(f"Getting entity with ID: {id}")
        return await self.repository.get(id)

    async def list(self, filters: Optional[dict] = None) -> list[T]:
        """List entities with optional filtering."""
        self.logger.info(f"Listing entities with filters: {filters}")
        return await self.repository.list(filters)

    async def update(self, id: str, entity: T) -> T:
        """Update an existing entity."""
        self.logger.info(f"Updating entity with ID: {id}")
        return await self.repository.update(id, entity)

    async def delete(self, id: str) -> bool:
        """Delete an entity by ID."""
        self.logger.info(f"Deleting entity with ID: {id}")
        return await self.repository.delete(id)

    async def search(self, query: str, **kwargs) -> list[T]:
        """Search for entities using a query string."""
        self.logger.info(f"Searching entities with query: {query}")
        return await self.repository.search(query, **kwargs)
