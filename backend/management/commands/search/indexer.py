import os
from typing import Dict, List

import pandas as pd
from sentence_transformers import SentenceTransformer

from core.utils import timeit
from infrastructure.data_streams import DataStreamDF
from infrastructure.index_store import ElasticsearchStore
from infrastructure.search import CosineEncoder


class EncodedDFLoader:
    """ """

    def __init__(self, model: SentenceTransformer, index_name: str, encoder=None, refresh: bool = False):
        """
        Load init data and encoder
        """
        self.index_name = index_name
        if not refresh and os.path.exists(self.dump_file_name):
            self.df = pd.read_parquet(self.dump_file_name)
        else:
            df = DataStreamDF().get_clean_data()
            encoder = encoder or CosineEncoder
            self.df = encoder.encode_df(model=model, df=df)
            self._create_dump()

    @property
    def dump_file_name(self) -> str:
        """
        Get the dump file name
        Returns:
            str: The dump file name
        """
        file_name = self.index_name + "_data.parquet"
        return os.path.join(os.path.dirname(__file__), file_name)

    @timeit
    def _create_dump(self):
        self.df.to_parquet(self.dump_file_name, compression="brotli")
        print("Dumping Data to Parquet: ", self.dump_file_name)

    def get_records(self) -> List[Dict]:
        return self.df.to_dict(orient="records")


class DataIndexer:
    @staticmethod
    @timeit
    def _update_index_store(index_name: str, records: list) -> None:
        print("Storing documents in Elasticsearch: ", len(records))
        es = ElasticsearchStore(index_name=index_name)
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")

    @classmethod
    def re_indexing(cls, model, index_name: str, refresh=False) -> None:
        obj = EncodedDFLoader(model=model, index_name=index_name, refresh=refresh)
        cls._update_index_store(index_name, obj.get_records())
