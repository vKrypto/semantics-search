from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class Repository(Generic[T], ABC):
    """Generic repository interface for database operations."""

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get an entity by ID."""

    @abstractmethod
    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """List entities with optional filtering."""

    @abstractmethod
    async def update(self, id: str, entity: T) -> T:
        """Update an existing entity."""

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an entity by ID."""

    @abstractmethod
    async def search(self, query: str, **kwargs) -> List[T]:
        """Search for entities using a query string."""
        pass
