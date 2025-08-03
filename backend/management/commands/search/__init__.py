from domain.interfaces.management import ManagementCommondBase

from infrastructure.index_store.indexer import DataIndexer
from management.commands.index_store import ReindexingCommand


class RefreshEmbeddingsCommand(ReindexingCommand):

    @classmethod
    async def execute(cls, **kwargs):
        DataIndexer.refresh_index_store(cls._model, index_name=cls._index_name, index_type=cls._index_type, refresh=True)
 
    def get_command_name(self) -> str:
        return "refresh-embeddings"


from typing import Optional

from sentence_transformers import SentenceTransformer

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.management import ManagementCommondBase
from infrastructure.index_store import ElasticsearchStore
from infrastructure.index_store.indexer import DataIndexer


class RefreshEmbeddingsCommand(ManagementCommondBase):
    
    _index_name = AppSettings.DEFAULT_INDEX_NAME
    _index_type = AppSettings.DEFAULT_INDEX_TYPE
    _model: Optional[SentenceTransformer] = None
    index_param = None

    # def __init__(self, index_param=None, **kwargs):
    #     self.index_param = index_param

    @classmethod
    async def initialize_resources(cls) -> None:
        """Initialize the sentence transformer model if not already initialized."""
        if cls._model is None:
            logger.info(f"Initializing sentence transformer model: {AppSettings.EMBEDDING_MODEL}")
            cls._model = SentenceTransformer(AppSettings.EMBEDDING_MODEL, cache_folder=AppSettings.MODEL_CACHE_DIR, local_files_only=False)

    @classmethod
    async def execute(cls, **kwargs) -> None:
        print(f"Re-indexing with param: {cls.index_param}, extra: {kwargs}")
        DataIndexer.re_indexing(cls._model, cls._index_name, refresh=True)
    
    @staticmethod
    def get_command_name() -> str:
        return "re-index-store"
    
    @classmethod
    async def release_resources(cls) -> None:
        """Release the sentence transformer model."""
        cls._model = None
