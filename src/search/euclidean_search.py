import numpy as np
from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector


class EuclideanQuerySelector:
    _es_connector = None  # type: ElasticsearchConnector

    def __init__(
        self,
        model: SentenceTransformer,
        index_name: str,
        query: str,
        top_k: int = 5,
        rerank_window: int = 20,
        max_distance: float = 1.5,
        **kwargs,
    ):
        self.index_name = index_name
        self.query_str = query
        self.top_k = top_k
        self.rerank_window = rerank_window
        self.max_distance = max_distance
        self.query_vector = model.encode(query.lower()).tolist()

        if EuclideanQuerySelector._es_connector is None:
            EuclideanQuerySelector._es_connector = ElasticsearchConnector(index_name=self.index_name)

    @property
    def search_query(self):
        return {
            "knn": {
                "field": "title_vectors",
                "query_vector": self.query_vector,
                "k": self.rerank_window,
                "num_candidates": self.rerank_window * 2,
            },
            "size": self.top_k,
            "_source": ["title", "data"],
            "rescore": [
                {
                    "window_size": self.rerank_window,
                    "query": {
                        "rescore_query": {
                            "function_score": {
                                "script_score": {
                                    "script": {
                                        "source": """
                                            double dist = 0;
                                            for (int i = 0; i < params.query_vector.length; ++i) {
                                                double diff = params.query_vector[i] - doc['title_vectors'][i];
                                                dist += diff * diff;
                                            }
                                            return -Math.sqrt(dist);
                                        """,
                                        "params": {"query_vector": self.query_vector},
                                    }
                                }
                            }
                        },
                        "query_weight": 0.0,
                        "rescore_query_weight": 1.0,
                    },
                }
            ],
        }

    def __iter__(self):
        res = self._es_connector.conn.search(index=self.index_name, body=self.search_query)
        hits = res["hits"]["hits"]
        return iter(hits)
