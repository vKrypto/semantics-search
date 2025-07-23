"""Abstract index store provider interface."""

from abc import ABC, abstractmethod
from typing import Dict, Iterable


class IndexStoreProvider(ABC):
    """Interface that all index store providers must implement."""

    @abstractmethod
    def add_documents(self, documents: Iterable[Dict]) -> None:
        """Add multiple documents to the index."""

    @abstractmethod
    def add_bulk_documents(self, documents: Iterable[Dict]) -> None:
        """Insert a batch of documents in the index."""

    @abstractmethod
    def reset_index(self) -> None:
        """Remove and recreate the index."""

    @abstractmethod
    def count(self) -> int:
        """Return the number of stored documents."""
