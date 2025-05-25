from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector
from utils import DataIndexer, timeit

# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")


DataIndexer.re_indexing(model=TRANSFORMER_MODEL, refresh=False)  # Re-index the data after the model is loaded


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

    res = es.conn.search(index=es.index_name, body=search_query)
    print(f"{query=}: {res=}")


# re_indexing()
# search_query("Brown")
