from typing import Iterable, List
from kafka import KafkaData
from faq import FAQData
from myntra import MyntraProductsData
from ornaz import OrnazProductsData


class Data:
    def __init__(self):
        self.data_sources:List[Iterable] = [
            KafkaData(),
            FAQData(), 
            MyntraProductsData(),
            OrnazProductsData()
        ]

    def __iter__(self) -> Iterable[str]:
        for data_source in self.data_sources:
            for item in data_source:
                yield item['title']



__all__ = ['Data']