import abc
from typing import AsyncGenerator, Iterable, List, Optional, Type

import numpy as np
from pandas import DataFrame
from sentence_transformers import SentenceTransformer

from core.logging.logger import logger
from core.utils import timeit
from domain.interfaces.search import SearchStrategy
from domain.models.search import SearchResult, StrategyType
from infrastructure.index_store import IndexStoreFactory

# TODO: temp fix
np.float_ = np.float64


class QuerySelector(abc.ABC):
    def search_query(self, *args, **kwargs): ...


class CosineQuerySelector:
    def __init__(self, vector_field: str = "search_vectors", top_k: int = 5, min_score: float = 0.30) -> None:
        self.top_k = top_k
        self.min_score = min_score
        self.vector_field = vector_field

    def search_query(self, query_vector: List[int]):
        return {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": f"1 + cosineSimilarity(params.query_vector, '{self.vector_field}')",
                        "params": {"query_vector": query_vector},
                    },
                }
            },
            "size": self.top_k,
            "min_score": 1 + self.min_score,  # cosine range [-1, 1] → [0, 2]
            "_source": ["title", "data"],
        }


class CosineEncoder:

    @staticmethod
    def _normalize(vec):
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else vec.tolist()

    @timeit
    @classmethod
    def encode_df(cls, model: SentenceTransformer, df: DataFrame) -> DataFrame:
        """
        Encode the data from the dataframe
        Args:
            df: The dataframe to encode
        """
        logger.info(f"Creating Embding for : {len(df)} entries")
        df["title_vectors"] = df["title"].apply(lambda x: cls._normalize(model.encode(x)))  # --> [-1, 1]
        return df


class CosineSearchStrategy(SearchStrategy, CosineEncoder):
    """Search strategy using cosine similarity."""

    # both are commonly being used, assuming they will be static
    _es_connector = None
    _qs: Optional[Type[QuerySelector]] = None

    def __init__(self, model: SentenceTransformer, index_name: str = "documents", **kwargs):
        """Initialize the cosine search strategy.

        Args:
            model: The sentence transformer model to use
            index_name: Name of the search index
        """
        self.model = model
        self.index_name = index_name

        if self._qs is None:
            CosineSearchStrategy._qs = CosineQuerySelector(**kwargs)
        if self._es_connector is None:
            CosineSearchStrategy._es_connector = IndexStoreFactory.create_provider(index_name=self.index_name)

    def search_query_vector(self, query_vector) -> Iterable[dict]:
        try:
            res = self._es_connector.conn.search(index=self.index_name, body=self._qs.search_query(query_vector))
            return iter(res["hits"]["hits"])
        except Exception as e:
            print(f"[Error] Query failed: {e}")
            return iter([])

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return -1
        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    async def search(self, query: str, raw_format: bool = False) -> AsyncGenerator[SearchResult, None]:
        """Perform a cosine similarity search.
        Returns:
            List of search results
        """
        query = self.clean_and_remove_stop_words(query)
        # Encode query and create vector
        query_vector = self._normalize(self.model.encode(query.lower()))
        res = self.search_query_vector(query_vector)
        for item in res:
            if not raw_format:
                item = {
                    "title": item.get("_source", {}).get("title", "No title"),
                    "description": item.get("_source", {}).get("data", "{}").get("description", "-NA-"),
                    "score": round(item.get("_score", 0) - 1, 2),  # converting to --> [-1, 1] scale again
                }
            yield item

    def get_strategy_name(self) -> Type[StrategyType]:
        return StrategyType.COSINE
