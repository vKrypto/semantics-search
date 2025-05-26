from .cosine_search import CosineQuerySelector
from .euclidean_search import EuclideanQuerySelector
from .hybrid_search import HybridQuerySelector


def get_default_search_class(index_name: str) -> type:
    if index_name == "euclidian_indexes":
        return EuclideanQuerySelector
    else:
        return CosineQuerySelector


__all__ = ["get_default_search_class", "CosineQuerySelector", "EuclideanQuerySelector", "HybridQuerySelector"]
