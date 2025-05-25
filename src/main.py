from pprint import pprint

from sentence_transformers import SentenceTransformer

from db_connectors import ElasticsearchConnector
from search import CosineQuerySelector
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


res = CosineQuerySelector(
    index_name=INDEX_NAME, query="I am getting multiple unusual messages how can I stop that?", top_k=4, min_score=0.30
)

for i in res:
    i["_score"] -= 1
    pprint(i)

# how to unsubscribe from marketing mailes
