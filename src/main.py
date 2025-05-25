from sentence_transformers import SentenceTransformer

from search import CosineQuerySelector

INDEX_NAME = "cosine_indexes"
# model = SentenceTransformer("all-MiniLM-L6-v2")
TRANSFORMER_MODEL = SentenceTransformer("all-mpnet-base-v2", local_files_only=True)
print("Model loaded successfully!")

# Re-index the data after the model is loaded
# DataIndexer.re_indexing(index_name=INDEX_NAME, model=TRANSFORMER_MODEL, refresh=False)
# print("Re-indexing done!")


def search_title(query: str):
    res = CosineQuerySelector(model=TRANSFORMER_MODEL, index_name=INDEX_NAME, query=query, min_score=0.33, top_k=4)
    return res
