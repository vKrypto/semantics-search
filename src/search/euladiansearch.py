import numpy as np
from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector


class EucladianQuerySelector:
    def __init__(
        self, model: SentenceTransformer, index_name: str, query: str, top_k: int = 1, min_score: float = 0.30
    ) -> None:
        self.index_name = index_name
        self.query_str = query
        self.top_k = top_k
        self.min_score = min_score
        self.query_vector = self._normalize(model.encode(query.lower()))
        self._es_connector = ElasticsearchConnector(index_name=self.index_name)

    @staticmethod
    def _normalize(vec):
        vec = np.array(vec)
        return (vec / np.linalg.norm(vec)).tolist()

    def __iter__(self) -> list:
        res = self._es_connector.conn.knn_search(
            index=self.index_name,
            knn={"field": "title_vectors", "query_vector": self.query_vector, "k": self.top_k, "num_candidates": 500},
            source=["title", "description"],
        )
        return res["hits"]["hits"]
