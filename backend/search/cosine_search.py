import numpy as np
from db_connectors import ElasticsearchConnector
from sentence_transformers import SentenceTransformer


class CosineQuerySelector:
    _es_connector = None  # type: ElasticsearchConnector

    def __init__(
        self,
        model: SentenceTransformer,
        index_name: str,
        query: str,
        top_k: int = 5,
        min_score: float = 0.30,
        vector_field: str = "title_vectors",
    ):
        self.index_name = index_name
        self.query_str = query
        self.top_k = top_k
        self.min_score = min_score
        self.vector_field = vector_field
        self.query_vector = self._normalize(model.encode(query.lower()))
        if CosineQuerySelector._es_connector is None:
            CosineQuerySelector._es_connector = ElasticsearchConnector(index_name=self.index_name)

    @staticmethod
    def _normalize(vec):
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else vec.tolist()

    @property
    def search_query(self):
        return {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": f"1 + cosineSimilarity(params.query_vector, '{self.vector_field}')",
                        "params": {"query_vector": self.query_vector},
                    },
                }
            },
            "size": self.top_k,
            "min_score": 1 + self.min_score,  # cosine range [-1, 1] → [0, 2]
            "_source": ["title", "data"],
        }

    def __iter__(self):
        try:
            res = self._es_connector.conn.search(index=self.index_name, body=self.search_query)
            return iter(res["hits"]["hits"])
        except Exception as e:
            print(f"[Error] Query failed: {e}")
            return iter([])
