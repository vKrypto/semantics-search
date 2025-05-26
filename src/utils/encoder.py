import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from data_streams import DataStreamDF

from .common import timeit

np.float_ = np.float64


class DFDataEncoder:
    dump_file_name = "all_data.parquet"
    dump_file_name = os.path.join(os.path.dirname(__file__), dump_file_name)
    df = None

    def __init__(self, refresh: bool, model: SentenceTransformer):
        if not refresh and os.path.exists(self.dump_file_name):
            self.df = pd.read_parquet(self.dump_file_name)
        else:
            df = DataStreamDF().get_clean_data()
            self.df = self._encode_data_from_df(df, model=model)
            self._create_dump()

    @staticmethod
    @timeit
    def _encode_data_from_df(df: pd.DataFrame, model: SentenceTransformer) -> pd.DataFrame:
        def normalize(vec):
            vec = np.array(vec)
            return (vec / np.linalg.norm(vec)).tolist()

        print("Creating Embding: ", len(df))
        # df["title_vectors"] = df["title"].apply(lambda x: model.encode(x).astype(float).tolist())
        df["title_vectors"] = df["title"].apply(lambda x: normalize(model.encode(x)))  # --> [-1, 1]
        return df

    @timeit
    def _create_dump(self):
        self.df.to_parquet(self.dump_file_name, compression="brotli")
        print("Dumping Data to Parquet: ", self.dump_file_name)

    def get_records(self) -> list:
        return self.df.to_dict(orient="records")
