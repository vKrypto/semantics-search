import json
import os
from dataclasses import dataclass
from typing import Iterator, Any


@dataclass
class OrnazProductsData(Iterator[Any]):
    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.json")
        with open(filepath) as f:
            self.data = json.load(f)["products"]
        self._iter = iter(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        item = self.data[next(self._iter)]["data"]  # raises StopIteration when done
        return {
            "title": item["url"],
            "description": item["pdp_url"].replace("/", " ").replace("-", " "),
        }
