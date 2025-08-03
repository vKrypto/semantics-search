from typing import Any, Dict, Generator, Iterable
from pandas import DataFrame
from core.utils import timeit

from .faq import FAQData
from .kafka import KafkaData
from .myntra import MyntraProductsData
from .ornaz import OrnazProductsData


class DataStreams:
    data_sources: Dict[str, Iterable[Dict[str, str]]] = {
        "100": KafkaData,
        "200": FAQData,
        "300": MyntraProductsData,
        "400": OrnazProductsData,
    }

    def __iter__(self) -> Generator[dict[str, int | str | dict[str, str]], Any, Any]:
        for source_index, data_source_class in self.data_sources.items():
            data_source = data_source_class()  # instantiate the data source
            source_data_index = 0
            for data in data_source:
                source_data_index += 1
                _id = "%0*d" % (6, source_data_index)  # tweak this numer when needed to scale
                title = data["key"].lower()
                l_int_id = int(source_index + _id)
                yield {"id": l_int_id, "key": title, "value": data}


class DataStreamDF(DataStreams):
    def _get_all_data(self) -> DataFrame:
        print("getting all documents..")
        return DataFrame(list(self))

    @staticmethod
    def _clean_data(df: DataFrame) -> DataFrame:
        print("cleaning documents: ", len(df))
        df.fillna(value="", inplace=True)
        return df

    @timeit
    def get_clean_data(self) -> DataFrame:
        return self._clean_data(self._get_all_data())
