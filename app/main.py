from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic","YOUR_ES_PASSWORD"),
    ca_certs="/.../elasticsearch-<version>/config/certs/http_ca.crt"
)
es.ping()