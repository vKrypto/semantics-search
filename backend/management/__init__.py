from domain.models.management import Command

from .commands.index_store import RefreshIndexStoreCommand
from .commands.search import RefreshEmbeddingsCommand
from .commands.data_streams import ValidateStreamsData, ValidateStreams
from .factory import ManagementCommandFactory

ManagementCommandFactory.register_command(Command.REFRESH_EMBEDDINGS, RefreshEmbeddingsCommand)
ManagementCommandFactory.register_command(Command.REFRESH_INDEX_STORE, RefreshIndexStoreCommand)
ManagementCommandFactory.register_command(Command.VALIDATE_STREAMS_DATA, ValidateStreamsData)
ManagementCommandFactory.register_command(Command.VALIDATE_STREAMS, ValidateStreams)


__all__ = ["ManagementCommandFactory"]
