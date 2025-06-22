"""Management strategy interface for management actions."""

from abc import ABC, abstractmethod


class ManagementCommondBase(ABC):
    @abstractmethod
    async def execute(self, **kwargs):
        """Execute the management action."""

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of the strategy."""
