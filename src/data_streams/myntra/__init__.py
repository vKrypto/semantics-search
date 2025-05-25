import json
import os
import pandas as pd
from dataclasses import dataclass
from typing import Iterator, Any


@dataclass
class MyntraProductsData(Iterator[Any]):
    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.csv")
        self.df = pd.read_csv(filepath)
        self._iter = iter(
            self.df[["ProductName", "Description"]].to_dict(orient="records")
        )  # convert to dict for easy iteration)

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._iter)  # raises StopIteration when done
        return {"title": item["ProductName"], "description": item["Description"]}
