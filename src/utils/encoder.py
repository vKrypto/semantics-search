import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from data_streams import DataStreamDF
from utils import timeit

np.float_ = np.float64


class DFDataEncoder:
    dump_file_name = "data.parquet"
    df = None

    def __init__(self, fresh: bool, model: SentenceTransformer):
        if not (fresh and os.path.exists(self.dump_file_name)):
            self.df = pd.read_parquet(self.dump_file_name)
        else:
            df = DataStreamDF().get_clean_data()
            self.df = self._encode_data_from_df(df, model=model)
            self._create_dump()

    @staticmethod
    @timeit
    def _encode_data_from_df(df: pd.DataFrame, model: SentenceTransformer) -> pd.DataFrame:
        print("Creating Embding: ", len(df))
        df["description_vectors"] = df["description"].apply(lambda x: model.encode(x).astype(float).tolist())
        return df

    @timeit
    def _create_dump(self):
        self.df.to_parquet(self.dump_file_name)

    def get_records(self) -> list:
        return self.df.to_dict(orient="records")
