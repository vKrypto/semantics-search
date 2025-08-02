from enum import Enum


class Command(Enum):
    REFRESH_EMBEDDINGS = "refresh-embeddings"
    REFRESH_INDEX_STORE = "refresh-index-store"
    VALIDATE_STREAMS = "validate-streams"
    VALIDATE_STREAMS_DATA = "validate-streams-data"
