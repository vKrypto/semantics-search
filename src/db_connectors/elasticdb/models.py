INDEX_MAPPINGS = {
    "test_indexes": {
        "properties":{
            "id":{
                "type":"long"
            },
            "title":{
                "type":"text"
            },
            "description":{
                "type":"text"
            },
            "description_vectors":{
                "type":"dense_vector",
                "dims": 768,
                "index":True,
                "similarity": "l2_norm" # euclidian similarity, we can use cosine based
            }

        }
    }
}