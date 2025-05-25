from pprint import pprint

from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector
from utils import DataIndexer, timeit

INDEX_NAME = "cosine_indexes"
# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")
DataIndexer.re_indexing(
    index_name=INDEX_NAME, model=TRANSFORMER_MODEL, refresh=True
)  # Re-index the data after the model is loaded
print("Re-indexing done!")


ES_CONNECTOR = ElasticsearchConnector(index_name=INDEX_NAME)


def search_query(query: str, top_k: int = 5) -> list:
    query_vector = [float(i) for i in TRANSFORMER_MODEL.encode(query.lower())]
    res = ES_CONNECTOR.conn.knn_search(
        index=ES_CONNECTOR.index_name,
        knn={"field": "title_vectors", "query_vector": query_vector, "k": top_k, "num_candidates": 500},
        source=["title", "description"],
    )
    # print(f"{query=}: {res=}")
    return res["hits"]["hits"]


class CosineQuerySelector:
    def __init__(self, query, top_k: int = 1, min_score: float = 0.30) -> None:
        self.query_str = query
        self.top_k = top_k
        self.min_score = min_score
        self.query_vector = [float(i) for i in TRANSFORMER_MODEL.encode(query.lower())]

    @property
    def search_query(self):
        return {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "1 + cosineSimilarity(params.query_vector, 'title_vectors')",  # [-1, 1] --> [0, 2]
                        "params": {"query_vector": self.query_vector},
                    },
                }
            },
            "size": self.top_k,
            "min_score": 1 + self.min_score,  # Only return documents with cosine similarity > 0.30
            "_source": ["title", "description"],
        }

    def __iter__(self) -> list:
        res = ES_CONNECTOR.conn.search(index=ES_CONNECTOR.index_name, body=self.search_query)
        return iter(res["hits"]["hits"])


res = CosineQuerySelector(query="I am getting multiple unusual messages how can I stop that?", top_k=4, min_score=0.30)
for i in res:
    i["_score"] -= 1
    pprint(i)

# how to unsubscribe from marketing mailes
