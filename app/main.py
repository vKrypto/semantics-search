import os
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200")

try:
    info = es.info()
    print("Connected to Elasticsearch:", info["version"]["number"])
except Exception as e:
    print("Failed:", e)
    os.exit(1)
