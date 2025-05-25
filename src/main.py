from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector
from utils import DataIndexer, timeit

INDEX_NAME = "cosine_indexes"
# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")
# DataIndexer.re_indexing(index_name=INDEX_NAME, model=TRANSFORMER_MODEL, refresh=False)  # Re-index the data after the model is loaded
# print("Re-indexing done!")


ES_CONNECTOR = ElasticsearchConnector(index_name=INDEX_NAME)


def search_query(query: str, top_k: int = 5) -> list:
    query_vector = [float(i) for i in TRANSFORMER_MODEL.encode(query.lower())]

    res = ES_CONNECTOR.conn.knn_search(
        index=ES_CONNECTOR.index_name,
        knn={"field": "description_vectors", "query_vector": query_vector, "k": top_k, "num_candidates": 500},
        source=["title", "description"],
    )

    # print(f"{query=}: {res=}")
    return res["hits"]["hits"]


def search_query_using_script_score(query: str, top_k: int = 5):
    query_vector = [float(i) for i in TRANSFORMER_MODEL.encode(query.lower())]
    search_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 + cosineSimilarity(params.query_vector, 'description_vectors')",
                    "params": {"query_vector": query_vector},
                },
            }
        },
        "size": top_k,
        "_source": ["title", "description"],
    }

    res = ES_CONNECTOR.conn.search(index=ES_CONNECTOR.index_name, body=search_query)

    # print(f"{query=}: {res=}")
    return res["hits"]["hits"]


from pprint import pprint

# re_indexing()


# res = search_query("Brown", top_k=2)
# for i in res:
#     pprint(i)
# print("-----------------------------")

res = search_query_using_script_score("Brown")
for i in res:
    pprint(i)
