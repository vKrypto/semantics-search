from enum import Enum


class IndexStoreProviderType(Enum):
    ELASTIC_DB: str = "elastic"
    FAISS: str = "faiss"
    PSQL: str = "psql"
