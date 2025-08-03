from domain.models.management import Command

from .commands.search import RefreshEmbeddingsCommand
from .commands.data_streams import ValidateStreamsData, ValidateStreams
from .commands.index_store import ReindexingCommand
from .factory import ManagementCommandFactory


ManagementCommandFactory.register_command(Command.REFRESH_EMBEDDINGS, RefreshEmbeddingsCommand)
ManagementCommandFactory.register_command(Command.VALIDATE_STREAMS_DATA, ValidateStreamsData)
ManagementCommandFactory.register_command(Command.VALIDATE_STREAMS, ValidateStreams)
ManagementCommandFactory.register_command(Command.REFRESH_INDEX_STORE, ReindexingCommand)

__all__ = ["ManagementCommandFactory"]
