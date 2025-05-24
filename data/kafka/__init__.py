import json
import os
from dataclasses import dataclass
from typing import Iterator, Any


@dataclass
class KafkaData(Iterator[Any]):
    def __post_init__(self):
        filepath = os.path.join(os.path.dirname(__file__), "data.json")
        with open(filepath) as f:
            self.data = json.load(f)
        self._iter = iter(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._iter)  # raises StopIteration when done
        return {"title": item, "description": item}
