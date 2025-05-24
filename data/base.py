from typing import Iterable
from kafka import KafkaData
from faq import FAQData

class Data:
    def __init__(self):
        self.data_sources = [KafkaData(), FAQData()]

    def __iter__(self) -> Iterable[str]:
        for data_source in self.data_sources:
            for item in data_source:
                yield item['title']



__all__ = ['Data']