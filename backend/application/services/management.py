import time
from typing import Optional

from core.logging.logger import logger
from management import ManagementCommandFactory


class ManagementService:
    """
    Example usage:

        result = await ManagementCommandFactory.execute_command(
            "refresh-embeddings",
            some_param="my_value",
            extra_param=123
        )
        # result will be "Embeddings refreshed"

        result2 = await ManagementCommandFactory.execute_command(
            "refresh-index-store",
            index_param="main_index",
            force=True
        )
        # result2 will be "Index store refreshed"
    """

    def __init__(self, command_name: str, **command_kwargs):
        self.command = ManagementCommandFactory.create_command(command_name, **command_kwargs)

    async def execute(self, **kwargs):
        return await self.command.execute(**kwargs)
