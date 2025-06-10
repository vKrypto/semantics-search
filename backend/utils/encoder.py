import os

import numpy as np
import pandas as pd
from data_streams import DataStreamDF
from sentence_transformers import SentenceTransformer

from .common import timeit

# temp fix
np.float_ = np.float64


class DFDataEncoder:
    df = None

    def __init__(self, model: SentenceTransformer, index_name: str, refresh: bool = False):
        self.index_name = index_name
        if not refresh and os.path.exists(self.dump_file_name):
            self.df = pd.read_parquet(self.dump_file_name)
        else:
            df = DataStreamDF().get_clean_data()
            self.df = self._encode_data_from_df(df, model=model)
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

    @staticmethod
    @timeit
    def _encode_data_from_df(df: pd.DataFrame, model: SentenceTransformer) -> pd.DataFrame:
        """
        Encode the data from the dataframe
        Args:
            df: The dataframe to encode
            model: The model to use for encoding
        """

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
