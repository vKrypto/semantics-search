from db_connectors import ElasticsearchConnector
from utils import timeit
from sentence_transformers import SentenceTransformer
from encoder import DFDataEncoder


# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")


class Indexer:
    @timeit
    def update_index_store(records: list):
        print("Storing documents in Elasticsearch: ", len(records))
        es = ElasticsearchConnector()
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")


def re_indexing():
    obj = DFDataEncoder(model=TRANSFORMER_MODEL, fresh=False)
    Indexer.update_index_store(obj.get_records())


def search_query(query):
    es = ElasticsearchConnector()
    query_vector = [float(i) for i in TRANSFORMER_MODEL.encode(query.lower())]
    # perform search
    search_query = {
        "knn": {
            "field": "description_vectors",
            "query_vector": query_vector,
            "k": 2,
            "num_candidates": 500,
        },
        "_source": ["title"],
    }

    res = es.conn.search(index=es.index.NAME, body=search_query)
    print(f"{query=}: {res=}")


re_indexing()
# search_query("Brown")
