import nltk

nltk.download("punkt_tab", force=True)
from nltk.tokenize import word_tokenize

tokens = word_tokenize("Your text here.")


from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", max_retries=3)

print(es.info())

