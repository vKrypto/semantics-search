from enum import Enum


class IndexStoreProviderType(Enum):
    """
    Index store provider type
    """

    ELASTIC_DB = "elastic"
    FAISS = "faiss"
    PSQL = "psql"
