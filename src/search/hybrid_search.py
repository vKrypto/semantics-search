from operator import itemgetter

import numpy as np
from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector


class HybridQuerySelector:
    """
    Do ANNSearch and rerank the results using Cosine Similarity.
    """

    _es_connector = None  # type: ElasticsearchConnector

    def __init__(
        self,
        model: SentenceTransformer,
        index_name: str,
        query: str,
        top_k: int = 5,
        rerank_k: int = 20,
        min_score: float = 0.30,
    ):
        self.index_name = index_name
        self.query_str = query
        self.top_k = top_k
        self.rerank_k = rerank_k
        self.min_score = min_score
        self.model = model
        self.query_vector = self._normalize(model.encode(query.lower()))
        if HybridQuerySelector._es_connector is None:
            HybridQuerySelector._es_connector = ElasticsearchConnector(index_name=self.index_name)

    @staticmethod
    def _normalize(vec):
        vec = np.array(vec)
        return (vec / np.linalg.norm(vec)).tolist()

    @property
    def ann_query(self):
        return {
            "knn": {
                "field": "title_vectors",
                "query_vector": self.query_vector,
                "k": self.rerank_k,
                "num_candidates": self.rerank_k * 2,
            },
            "_source": ["title", "data", "title_vectors"],
        }

    def _cosine_similarity(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return -1
        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    def __iter__(self):
        # Step 1: ANN retrieval
        res = self._es_connector.conn.search(index=self.index_name, body=self.ann_query)
        hits = res["hits"]["hits"]

        # Step 2: Cosine reranking
        reranked = []
        for hit in hits:
            vec = hit["_source"].get("title_vectors")
            score = self._cosine_similarity(self.query_vector, vec)
            if score >= self.min_score:
                reranked.append((score, hit))

        reranked.sort(reverse=True, key=itemgetter(0))
        top_hits = [hit for _, hit in reranked[: self.top_k]]

        return iter(top_hits)
