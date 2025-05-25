from db_connectors import ElasticsearchConnector
from utils import DFDataEncoder, timeit


class DataIndexer:

    @staticmethod
    @timeit
    def update_index_store(records: list):
        print("Storing documents in Elasticsearch: ", len(records))
        es = ElasticsearchConnector()
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")

    @classmethod
    def re_indexing(cls, model, refresh=False):
        obj = DFDataEncoder(model=model, fresh=refresh)
        cls.update_index_store(obj.get_records())
