from domain.models.index_store import IndexStoreProviderType

from .elastic_db import ElasticsearchStore
from .factory import IndexStoreFactory

# Register providers
IndexStoreFactory.register_provider(IndexStoreProviderType.ELASTIC_DB, ElasticsearchStore)

__all__ = ["IndexStoreFactory", "ElasticsearchStore", "IndexStoreProviderType"]
