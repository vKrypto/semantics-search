from domain.models.management import Command

from .commands.index_store import RefreshIndexStoreCommand
from .commands.search import RefreshEmbeddingsCommand
from .factory import ManagementCommandFactory

ManagementCommandFactory.register_command(Command.REFRESH_EMBEDDINGS, RefreshEmbeddingsCommand)
ManagementCommandFactory.register_command(Command.REFRESH_INDEX_STORE, RefreshIndexStoreCommand)


__all__ = ["ManagementCommandFactory"]
