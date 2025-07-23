from typing import Optional

from sentence_transformers import SentenceTransformer

from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.interfaces.management import ManagementCommondBase
from .indexer import DataIndexer


class RefreshEmbeddingsCommand(ManagementCommondBase):
    """Command to regenerate embeddings and refresh the index store."""

    _index_name = AppSettings.DEFAULT_INDEX_NAME
    _model: Optional[SentenceTransformer] = None

    def __init__(self, some_param=None, **kwargs):
        self.some_param = some_param

    @classmethod
    def _load_model(cls) -> None:
        if cls._model is None:
            logger.info(f"Initializing sentence transformer model: {AppSettings.EMBEDDING_MODEL}")
            cls._model = SentenceTransformer(AppSettings.EMBEDDING_MODEL, local_files_only=True)

    async def execute(self, **kwargs):
        self._load_model()
        print(f"Refreshing embeddings with param: {self.some_param}, extra: {kwargs}")
        DataIndexer.re_indexing(self._model, self._index_name, refresh=True)
        return "Embeddings refreshed"

    def get_command_name(self) -> str:
        return "refresh-embeddings"
