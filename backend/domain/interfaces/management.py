"""Management strategy interface for management actions."""

from abc import ABC, abstractmethod


class ManagementCommondBase(ABC):
    COMMOND_NAME: str = ...
    # Make sure ManagementCommondBase does not actually acept any parameters in its constructor from command line

    async def initialize_resources(*args, **kwargs):
        pass

    @abstractmethod
    async def execute(*args, **kwargs):
        """Execute the management action."""

    @abstractmethod
    async def get_command_name(*args) -> str:
        """Return the name of the strategy."""

    async def release_resources(*args, **kwargs) -> None:
        """Release any resources held by the strategyin initialize_resouurces."""
        pass
