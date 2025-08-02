"""Management strategy interface for management actions."""

from abc import ABC, abstractmethod


class ManagementCommondBase(ABC):
    # Make sure ManagementCommondBase does not actually acept any parameters in its constructor from command line

    @abstractmethod
    async def execute(self, **kwargs):
        """Execute the management action."""

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of the strategy."""
