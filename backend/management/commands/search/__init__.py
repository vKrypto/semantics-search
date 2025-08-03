# from infrastructure.index_store.indexer import DataIndexer
# from management.commands.index_store import ReindexingCommand
# from domain.models.management import Command

# class RefreshEmbeddingsCommand(ReindexingCommand):
#     COMMOND_NAME = Command.REFRESH_INDEX_STORE

#     @classmethod
#     async def execute(cls, **kwargs):
#         DataIndexer.refresh_index_store(cls._model, index_name=cls._index_name, index_type=cls._index_type, refresh=True)
 