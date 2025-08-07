import os
import json
import pandas as pd
from typing import Dict, List
from sentence_transformers import SentenceTransformer

from core.config.settings import AppSettings
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
            self.df["value"] = self.df["value"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
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
        return os.path.join(AppSettings.MODEL_CACHE_DIR, file_name)

    @timeit
    def _create_dump(self):
        for col in ["value"]:
            if self.df[col].apply(lambda x: isinstance(x, dict)).any():
                self.df[col] = self.df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
        self.df.to_parquet(self.dump_file_name, compression="brotli")
        print("Dumping Data to Parquet: ", self.dump_file_name)

    def get_records(self) -> List[Dict]:
        print("Getting records from DataFrame: ", len(self.df))
        return self.df.to_dict(orient="records")


class DataIndexer:

    @classmethod
    def refresh_index_store(cls, model, index_name: str = None, index_type: str = None, refresh: bool = False) -> None:
        # getting encoded embedding records
        if refresh:
            print("Refreshing index store")
        records = cls.re_indexing(model, index_name=index_name, refresh=refresh)

        # reset index and add documents
        print("Refreshing documents in Elasticsearch: ", len(records))
        es = ElasticsearchStore(index_name=index_name, index_type=index_type)
        es.reset_index()
        es.add_bulk_documents(records)
        print(f"Re-indexing done!, total indexed documents: {es.count()}")

    @staticmethod
    @timeit
    def re_indexing(model, index_name: str, refresh: bool = False) -> None:
        obj = EncodedDFLoader(model=model, index_name=index_name, refresh=refresh)
        return obj.get_records()
