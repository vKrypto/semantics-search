import os
from pandas import read_csv
from dataclasses import dataclass
from domain.interfaces.data_streams import DataStream


@dataclass
class MyntraProductsData(DataStream):
    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.csv")
        self.df = read_csv(filepath)
        self._iter = iter(self.df[["ProductName", "Description"]].to_dict(orient="records"))  # convert to dict for easy iteration)

    def __next__(self):
        item = next(self._iter)  # raises StopIteration when done
        return {"key": item["ProductName"], "value": item}

    def __iter__(self):
        return self

    def __type__(self):
        return self.__class__.__name__
