import json
import os
from domain.interfaces.data_streams import DataStream
from dataclasses import dataclass


@dataclass
class FAQData(DataStream):

    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.json")
        with open(filepath) as f:
            self.data = json.load(f)
        self._iter = iter(self.data)

    def __next__(self):
        item = next(self._iter)  # raises StopIteration when done
        return {"key": item["question"], "value": item}

    def __iter__(self):
        return self
