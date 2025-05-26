from db_connectors import ElasticsearchConnector
from utils import DFDataEncoder, timeit


class DataIndexer:

    @staticmethod
    @timeit
    def update_index_store(index_name: str, records: list):
        print("Storing documents in Elasticsearch: ", len(records))
        es = ElasticsearchConnector(index_name=index_name)
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")

    @classmethod
    def re_indexing(cls, model, index_name: str, refresh=False):
        obj = DFDataEncoder(model=model, index_name=index_name, refresh=refresh)
        cls.update_index_store(index_name, obj.get_records())
