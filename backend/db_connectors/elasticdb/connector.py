from typing import Dict, Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import BulkIndexError, bulk

from .models import INDEX_MAPPINGS


class ElasticsearchConnector:
    URL = "http://localhost:9200"
    _conn = None
    index_name = ...
    index_mapping = ...

    def __init__(self, index_name: str) -> None:
        self.index_name = index_name
        if index_name not in INDEX_MAPPINGS:
            raise ValueError(f"Invalid index name: {index_name}, available options: {list(INDEX_MAPPINGS.keys())}!")
        self.index_mapping = INDEX_MAPPINGS[index_name]

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
            self.conn.indices.create(index=self.index_name, mappings=self.index_mapping)
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
        except BulkIndexError as e:
            try:
                caused = e.errors[0]["index"]["error"]["caused_by"]
                print(f"Bulk insert error: {caused['type']}: {caused['reason']}")
            except Exception as e:
                pass
            print("Bulk insert error:", str(e))
        return

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
