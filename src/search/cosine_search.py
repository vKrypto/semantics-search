import numpy as np
from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector


class CosineQuerySelector:
    _es_connector = None  # type: ElasticsearchConnector

    def __init__(
        self, model: SentenceTransformer, index_name: str, query: str, top_k: int = 1, min_score: float = 0.30
    ) -> None:
        self.index_name = index_name
        self.query_str = query
        self.top_k = top_k
        self.min_score = min_score
        self.query_vector = self._normalize(model.encode(query.lower()))
        if CosineQuerySelector._es_connector is None:  # Check if ElasticsearchConnector is already initialized
            CosineQuerySelector._es_connector = ElasticsearchConnector(index_name=self.index_name)

    @staticmethod
    def _normalize(vec):
        vec = np.array(vec)
        return (vec / np.linalg.norm(vec)).tolist()

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
        res = self._es_connector.conn.search(index=self.index_name, body=self.search_query)
        return iter(res["hits"]["hits"])
