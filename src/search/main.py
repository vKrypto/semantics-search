from typing import Iterable

from sentence_transformers import SentenceTransformer

from utils import DataIndexer

from .cosine_search import CosineQuerySelector
from .euclidean_search import EuclideanQuerySelector
from .hybrid_search import HybridQuerySelector


def get_default_search_class(index_name: str) -> type:
    if index_name == "euclidian_indexes":
        return EuclideanQuerySelector
    else:
        return CosineQuerySelector


INDEX_NAME = "cosine_indexes"
# INDEX_NAME = "euclidian_indexes"
# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")


def re_index(refresh: bool = False) -> None:
    # Re-index the data after the model is loaded
    DataIndexer.re_indexing(index_name=INDEX_NAME, model=TRANSFORMER_MODEL, refresh=refresh)
    print("Re-indexing done!")


def search_title(query: str, raw_format: bool = False) -> Iterable[dict]:
    """
    Search the title of the documents
    Args:
        query: The query to search for
        format_res: Whether to format the results
    Returns:
        A list of results
    """
    query = query.lower().strip().replace("  ", " ")
    QuerySelector_cls = get_default_search_class(INDEX_NAME)
    res = QuerySelector_cls(model=TRANSFORMER_MODEL, index_name=INDEX_NAME, query=query, min_score=0.33, top_k=4)
    for item in res:
        if not raw_format:
            item = {
                "title": item.get("_source", {}).get("title", "No title"),
                "description": item.get("_source", {}).get("data", "{}").get("description", "-NA-"),
                "score": round(item.get("_score", 0) - 1, 2),  # converting to --> [-1, 1] scale again
            }
        yield item


def search_query_and_create_context(query: str) -> str:
    """
    Search the title of the documents and create a context
    Args:
        query: The query to search for
    Returns:
        A string of the context
    """
    res = search_title(query)
    return "\n".join([f"Q: {item['title']}\nA: {item['description']}" for item in res])


def test_search():
    """
    [{'_index': 'cosine_indexes', '_id': '200000042', '_score': 1.3449435,
        '_source': {
            'title': 'how do i opt out of marketing emails?',
            'data': {'description': "click 'unsubscribe' at the bottom of any marketing email."}
        }
    }]
    """
    query = "I am getting multiple unusual messages how can I stop that?"
    res = search_title(query)
    return list(res)


if __name__ == "__main__":
    test_search()
