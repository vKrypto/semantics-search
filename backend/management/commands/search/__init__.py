from infrastructure.index_store.indexer import DataIndexer
from management.commands.index_store import ReindexingCommand


class RefreshEmbeddingsCommand(ReindexingCommand):

    @classmethod
    async def execute(cls, **kwargs):
        DataIndexer.refresh_index_store(cls._model, index_name=cls._index_name, index_type=cls._index_type, refresh=True)
 
    def get_command_name(self) -> str:
        return "refresh-embeddings"
