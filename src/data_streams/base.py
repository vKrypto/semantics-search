from typing import Dict, Iterable

import pandas as pd

from utils import timeit

from .faq import FAQData
from .kafka import KafkaData
from .myntra import MyntraProductsData
from .ornaz import OrnazProductsData


class DataStream:
    def __init__(self):
        self.data_sources: Dict[str, Iterable[Dict[str, str]]] = {
            "100": KafkaData(),
            "200": FAQData(),
            "300": MyntraProductsData(),
            "400": OrnazProductsData(),
        }

    def __iter__(self) -> Iterable[str]:
        for source_index, data_source in self.data_sources.items():
            source_data_index = 0
            for item in data_source:
                source_data_index += 1
                _id = "%0*d" % (6, source_data_index)
                data = {k: v.lower() for k, v in item.items()}
                title = data.pop("title", "")
                l_int_id = int(source_index + _id)
                yield {"id": l_int_id, "title": title, "data": data}


class DataStreamDF(DataStream):

    def _get_all_data(self) -> pd.DataFrame:
        print("getting all documents..")
        return pd.DataFrame(list(self))

    @staticmethod
    def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
        print("cleaning documents: ", len(df))
        df.fillna(value="", inplace=True)
        return df

    @timeit
    def get_clean_data(self) -> pd.DataFrame:
        return self._clean_data(self._get_all_data())
