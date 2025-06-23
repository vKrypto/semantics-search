from domain.interfaces.management import ManagementCommondBase

from .indexer import DataIndexer


class RefreshEmbeddingsCommand(ManagementCommondBase):
    def __init__(self, some_param=None, **kwargs):
        self.some_param = some_param

    async def execute(self, **kwargs):
        # Use self.some_param and kwargs for logic
        print(f"Refreshing embeddings with param: {self.some_param}, extra: {kwargs}")
        DataIndexer.re_indexing()
        return "Embeddings refreshed"

    def get_command_name(self) -> str:
        return "refresh-embeddings"
