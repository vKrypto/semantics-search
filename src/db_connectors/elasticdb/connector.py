from typing import Dict, Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from .models import INDEX_MAPPINGS


class BaseIndex:
    NAME: str = ...
    MAPPING: dict = ...


class DefaultIndex(BaseIndex):
    NAME: str = "test_indexes"
    MAPPING: dict = INDEX_MAPPINGS[NAME]


class ElasticsearchConnector:
    URL = "http://localhost:9200"
    _conn = None

    def __init__(self, index: BaseIndex = None):
        self.index = index or DefaultIndex

    @property
    def index_name(self) -> str:
        return self.index.NAME

    @property
    def conn(self) -> Elasticsearch:
        self._conn = self._conn or self.get_es_connection()
        return self._conn

    def get_es_connection(self) -> Elasticsearch:
        es_conn = Elasticsearch(self.URL, timeout=60, max_retries=3, retry_on_timeout=True)
        try:
            info = es_conn.info()
            print("Connected to Elasticsearch:", info["version"]["number"])
        except Exception as e:
            print("Failed:", e)
            raise
        return es_conn

    def _create_index(self):
        if not self.conn.indices.exists(index=self.index_name):
            self.conn.indices.create(index=self.index_name, mappings=self.index.MAPPING)
            print(f"Index '{self.index_name}' created")

    def add_documents(self, documents: Iterable[Dict]) -> None:
        self._create_index()
        print(f"Adding documents... {len(documents)} documents")
        for record in documents:
            try:
                self.conn.index(index=self.index_name, document=record, id=record["id"])
                print("added document:", record["id"])
            except Exception as e:
                print("error", str(e))

    def add_bulk_documents(self, documents: Iterable[Dict]) -> None:
        self._create_index()
        print(f"Adding documents... {len(documents)} documents")
        actions = [{"_index": self.index_name, "_id": doc["id"], "_source": doc} for doc in documents]
        try:
            success, failed = bulk(self.conn, actions)
            print(f"Bulk insert completed: {success} succeeded")
        except Exception as e:
            print("Bulk insert error:", str(e))

    def reset_index(self) -> None:
        if self.conn.indices.exists(index=self.index_name):
            self.conn.indices.delete(index=self.index_name)
            print(f"Index '{self.index_name}' deleted")
            self._create_index()

    def __del__(self):
        if self._conn:
            self.conn.close()

    def count(self) -> int:
        return self.conn.count(index=self.index_name)
