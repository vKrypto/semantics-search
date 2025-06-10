INDEX_MAPPINGS = {
    "euclidian_indexes": {
        "properties": {
            "id": {"type": "long"},
            "title": {"type": "text"},
            "data": {"type": "object", "properties": {"title": {"type": "text"}, "description": {"type": "text"}}},
            "title_vectors": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",  # euclidian similarity, we can use cosine based
            },
        }
    },
    "cosine_indexes": {
        "properties": {
            "id": {"type": "long"},
            "title": {"type": "text"},
            "data": {"type": "object", "properties": {"title": {"type": "text"}, "description": {"type": "text"}}},
            "title_vectors": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine",  # cosine similarity to get refine results with score
            },
        }
    },
}
