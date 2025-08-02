import json
import os
from dataclasses import dataclass
from domain.interfaces.data_streams import DataStream


@dataclass
class OrnazProductsData(DataStream):
    # use as a example to refresh from live data

    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.json")
        with open(filepath) as f:
            self.data = json.load(f)["products"]
        self._iter = iter(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        item = self.data[next(self._iter)]["data"]  # raises StopIteration when done
        return {"key": item["url"], "value": item}
