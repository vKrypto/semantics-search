from typing import Optional

from sentence_transformers import SentenceTransformer

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.management import ManagementCommondBase
from infrastructure.index_store import ElasticsearchStore
from management.commands.search.indexer import EncodedDFLoader


class RefreshIndexStoreCommand(ManagementCommondBase):

    _index_name = AppSettings.DEFAULT_INDEX_NAME
    _model: Optional[SentenceTransformer] = None

    def __init__(self, index_param=None, **kwargs):
        self.index_param = index_param

    @classmethod
    def _initialize_resource(cls) -> None:
        """Initialize the sentence transformer model if not already initialized."""
        if cls._model is None:
            logger.info(f"Initializing sentence transformer model: {AppSettings.EMBEDDING_MODEL}")
            cls._model = SentenceTransformer(AppSettings.EMBEDDING_MODEL, local_files_only=True)

    async def execute(self, **kwargs) -> None:
        print(
            f"Refreshing index store with param: {self.index_param}, extra: {kwargs}"
        )
        await self.re_indexing(self._model, self._index_name, refresh=True)

    def get_command_name(self) -> str:
        return "refresh-index-store"

    @staticmethod
    def _update_index_store(index_name: str, records: list):
        print("Storing documents in Elasticsearch: ", len(records))
        es = ElasticsearchStore(index_name=index_name)
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")

    async def re_indexing(self, model, index_name: str, refresh: bool = False) -> None:
        loader = EncodedDFLoader(model=model, index_name=index_name, refresh=refresh)
        self._update_index_store(index_name, loader.get_records())

    @classmethod
    def _release_resource(cls) -> None:
        """Initialize the sentence transformer model if not already initialized."""
        cls._model = None
